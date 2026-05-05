"""Admin login endpoint: POST /api/admin/login → returns a Bearer token."""
from flask import Blueprint, request, jsonify
from flask_security.utils import verify_password
from invenio_accounts.proxies import current_datastore
from invenio_db import db
from invenio_oauth2server.models import Token

blueprint = Blueprint("admin_auth", __name__, url_prefix="/admin")


@blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    user = current_datastore.get_user(email)
    if not user or not user.active or not verify_password(password, user.password):
        return jsonify({"message": "Invalid credentials."}), 401

    role_names = {r.name for r in user.roles}
    if "administration" not in role_names and "admin" not in role_names:
        return jsonify({"message": "Access denied: admin role required."}), 403

    # create a short-lived personal token named "admin-ui-session"
    # (reuse existing one if present to avoid accumulation)
    existing = Token.query.filter_by(
        user_id=user.id, is_personal=True
    ).filter(Token.client.has(name="admin-ui-session")).first()

    if existing:
        token_str = existing.access_token
    else:
        token = Token.create_personal(
            name="admin-ui-session",
            user_id=user.id,
            scopes=[],
            is_internal=True,
        )
        db.session.commit()
        token_str = token.access_token

    return jsonify({
        "token": token_str,
        "email": user.email,
        "user_id": user.id,
    }), 200
