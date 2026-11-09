#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$PWD}"
REPO="$(cd "$REPO" && pwd)"
[[ -f "$REPO/run.sh" && -f "$REPO/invenio.cfg" && -d "$REPO/.venv" ]] || {
    echo 'ERROR: Pass the path to an installed CESNET Invenio repository.' >&2
    exit 1
}

if ! grep -q 'from invenio_i18n import lazy_gettext as _lab_' "$REPO/invenio.cfg"; then
    [[ -e "$REPO/invenio.cfg.before-lab-setup" ]] || cp "$REPO/invenio.cfg" "$REPO/invenio.cfg.before-lab-setup"
    cat >> "$REPO/invenio.cfg" <<'ROLECFG'

from invenio_i18n import lazy_gettext as _lab_
if 'COMMUNITIES_ROLES' in globals():
    if not any(x['name'] == 'submitter' for x in COMMUNITIES_ROLES):
        COMMUNITIES_ROLES.insert(2, dict(
            name='submitter', title=_lab_('Submitter'),
            description=_lab_('Can submit records for review.')))
    for _r in COMMUNITIES_ROLES:
        if _r['name'] == 'owner':
            _r.setdefault('can_manage_roles', [])
            if 'submitter' not in _r['can_manage_roles']:
                _r['can_manage_roles'].append('submitter')
ROLECFG
fi

SEED_PY="$(mktemp "$REPO/.seed-users.XXXXXXXX.py")"
chmod 600 "$SEED_PY"
trap 'rm -f "$SEED_PY"' EXIT
cat > "$SEED_PY" <<'PYTHON'
from datetime import datetime, timezone
from flask import current_app
from flask_security.utils import hash_password, verify_password
from invenio_accounts.models import Role, User
from invenio_access.models import ActionRoles
from invenio_access.permissions import superuser_access, system_identity
from invenio_administration.permissions import administration_access_action
from invenio_communities.communities.records.api import Community
from invenio_communities.members.records.models import MemberModel
from invenio_communities.proxies import current_communities
from invenio_db import db
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_search import current_search_client
from invenio_search.utils import build_alias_name
from invenio_users_resources.proxies import current_users_service
from invenio_users_resources.records.api import UserAggregate

PASSWORD = '1234'
USERS = {
    'admin': None,
    'curator1': ('lab-community-1', 'curator'),
    'submitter1': ('lab-community-1', 'submitter'),
    'member1': ('lab-community-1', 'member'),
    'curator2': ('lab-community-2', 'curator'),
    'submitter2': ('lab-community-2', 'submitter'),
    'member2': ('lab-community-2', 'member'),
}
COMMUNITIES = {
    'lab-community-1': 'Laboratory 1',
    'lab-community-2': 'Laboratory 2',
}

if not current_app.config.get('ACCOUNTS_LOCAL_LOGIN_ENABLED', True):
    raise RuntimeError('Local password login is disabled in invenio.cfg')

configured_roles = {r['name'] for r in current_app.config.get('COMMUNITIES_ROLES', [])}
assert {'owner', 'curator', 'submitter', 'member'} <= configured_roles, configured_roles

store = current_app.extensions['security'].datastore
accounts = {}
for name in USERS:
    email = f'{name}@example.org'
    user = User.query.filter_by(email=email).one_or_none()
    if user is None:
        user = store.create_user(
            email=email, username=f'invenio_lab_{name}',
            password=hash_password(PASSWORD), active=True,
            confirmed_at=datetime.now(timezone.utc),
        )
        print(f'CREATED {email}')
    else:
        user.password = hash_password(PASSWORD)
        user.active = True
        user.confirmed_at = user.confirmed_at or datetime.now(timezone.utc)
        print(f'UPDATED {email}')
    user.verified_at = user.verified_at or datetime.now(timezone.utc)
    db.session.add(user)
    db.session.commit()
    assert user.active and user.confirmed_at and user.verified_at
    assert verify_password(PASSWORD, user.password)
    accounts[name] = user

user_indexer = current_users_service.indexer
for user in accounts.values():
    user_indexer.index(UserAggregate.get_record(user.id))
user_indexer.refresh(index=UserAggregate.index)
for user in accounts.values():
    doc = current_search_client.get(index=build_alias_name(UserAggregate.index._name), id=str(user.id))['_source']
    assert doc['active'] and doc['confirmed']
    print(f'INDEXED {user.email} (id={user.id})')

admin = accounts['admin']
for role_name, action in (
    ('admin', superuser_access),
    ('administration', administration_access_action),
):
    role = Role.query.filter_by(name=role_name).one_or_none()
    if role is None:
        role = store.create_role(id=role_name, name=role_name)
        db.session.commit()
    if role not in admin.roles:
        store.add_role_to_user(admin, role)
        db.session.commit()
    rule = ActionRoles.query.filter_by(
        role_id=role.id, action=action.value, argument=None, exclude=False
    ).one_or_none()
    if rule is None:
        db.session.add(ActionRoles.allow(action, role_id=role.id))
        db.session.commit()

service = current_communities.service
community_ids = {}
for slug, title in COMMUNITIES.items():
    try:
        community = Community.pid.resolve(slug)
        cid = community.id
        print(f'EXISTING COMMUNITY {slug}')
    except PIDDoesNotExistError:
        result = service.create(system_identity, {
            'slug': slug,
            'metadata': {'title': title},
            'access': {
                'visibility': 'restricted',
                'members_visibility': 'restricted',
                'record_submission_policy': 'closed',
            },
        })
        cid = result._record.id
        print(f'CREATED COMMUNITY {slug}')
    community_ids[slug] = cid

assignments = [
    (accounts['admin'], slug, 'owner') for slug in COMMUNITIES
] + [
    (accounts[name], community, role)
    for name, spec in USERS.items() if spec is not None
    for community, role in [spec]
]

for user, slug, role in assignments:
    cid = community_ids[slug]
    member = MemberModel.query.filter_by(
        community_id=cid, user_id=user.id
    ).one_or_none()
    data = {'members': [{'type': 'user', 'id': str(user.id)}], 'role': role}
    if member is None:
        service.members.add(system_identity, cid, data)
    elif not member.active:
        raise RuntimeError(f'Inactive/invited membership: {user.email}, {slug}')
    elif member.role != role:
        service.members.update(system_identity, cid, data, refresh=True)
    actual = MemberModel.query.filter_by(
        community_id=cid, user_id=user.id, active=True
    ).one()
    assert actual.role == role
    print(f'MEMBER {user.email} -> {slug} / {role}')

for user in accounts.values():
    user_indexer.index(UserAggregate.get_record(user.id))
user_indexer.refresh(index=UserAggregate.index)
for user in accounts.values():
    assert current_search_client.get(index=build_alias_name(UserAggregate.index._name), id=str(user.id))['found']
    assert verify_password(PASSWORD, user.password)

print('\nDONE: 7 active, confirmed and indexed users; 2 communities; 8 memberships.')
print('LOGINS: ' + ', '.join(f'{name}@example.org' for name in USERS))
print('PASSWORD FOR ALL USERS: 1234 (LAB ONLY)')
PYTHON

cd "$REPO"
export SEED_PY
./run.sh invenio shell --no-term-title -c \
    'import os; p=os.environ["SEED_PY"]; exec(compile(open(p, encoding="utf-8").read(), p, "exec"))'

