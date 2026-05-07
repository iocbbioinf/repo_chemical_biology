"""Bulk creation endpoint for spectrum records."""

from concurrent.futures import ThreadPoolExecutor, as_completed

from flask import current_app, g, jsonify
from flask_resources import resource_requestctx, route
from invenio_records_resources.resources.records.resource import request_data

# Maximum number of threads for parallel draft creation and publishing.
_BULK_WORKERS = 8


class BulkCreateResourceMixin:
    """Adds POST /api/spectrum/records/bulk — atomic create+publish of multiple records."""

    def create_url_rules(self):
        rules = super().create_url_rules()
        rules.append(route("POST", "/spectrum/records/bulk", self.bulk_create))
        return rules

    @request_data
    def bulk_create(self):
        """Create and publish multiple spectrum records atomically.

        Accepts a JSON array of record payloads. All records are created as
        drafts in parallel, then all published in parallel. If any step fails
        every already-created draft is deleted before returning the error
        (full rollback).

        Request body::

            [
                {"metadata": {...}, "files": {"enabled": false}},
                ...
            ]

        Returns HTTP 201 with the list of published records on success, or HTTP
        422 with the failing index and error message on rollback.
        """
        identity = g.identity
        records = resource_requestctx.data

        if not isinstance(records, list):
            return jsonify({"message": "Request body must be a JSON array."}), 400
        if not records:
            return jsonify({"message": "Record list is empty."}), 400

        published = self.service.bulk_create(identity, records)  # type: ignore[attr-defined]
        return jsonify(published), 201


class BulkCreateServiceMixin:
    """Adds bulk_create() to the record service."""

    def bulk_create(self, identity, records):
        """Create and publish all records in parallel with full rollback on any failure.

        Phase 1 – create drafts in parallel (up to _BULK_WORKERS threads).
        Phase 2 – publish drafts in parallel (up to _BULK_WORKERS threads).

        If any future in either phase raises, all collected draft ids are deleted
        via _rollback_drafts() and the original exception is re-raised as HTTP 422.

        Returns a list of published record dicts (order matches input) on success.
        """
        from flask import abort

        app = current_app._get_current_object()

        def create_one(idx, data):
            # Each thread needs its own app context for db.session (scoped per thread).
            with app.app_context():
                draft = self.create(identity, data)
                return idx, draft.id

        def publish_one(idx, draft_id):
            with app.app_context():
                record = self.publish(identity, draft_id)
                return idx, record.to_dict()

        workers = min(_BULK_WORKERS, len(records))

        # Phase 1: create all drafts in parallel
        draft_ids = [None] * len(records)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(create_one, idx, data): idx for idx, data in enumerate(records)}
            for future in as_completed(futures):
                try:
                    idx, draft_id = future.result()
                    draft_ids[idx] = draft_id
                except Exception as exc:
                    pool.shutdown(wait=True, cancel_futures=True)
                    self._rollback_drafts([d for d in draft_ids if d is not None])
                    abort(422, f"Record at index {futures[future]} failed during draft creation: {exc}")

        # Phase 2: publish all drafts in parallel
        published = [None] * len(records)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(publish_one, idx, draft_id): idx for idx, draft_id in enumerate(draft_ids)}
            for future in as_completed(futures):
                try:
                    idx, record_dict = future.result()
                    published[idx] = record_dict
                except Exception as exc:
                    pool.shutdown(wait=True, cancel_futures=True)
                    self._rollback_drafts(draft_ids)
                    abort(422, f"Record at index {futures[future]} failed during publish: {exc}")

        return published

    def _rollback_drafts(self, draft_ids):
        """Delete all drafts (and published records) in parallel — best effort."""
        from invenio_access.permissions import system_identity

        app = current_app._get_current_object()

        def delete_one(draft_id):
            with app.app_context():
                try:
                    self.delete_draft(system_identity, draft_id)
                except Exception:
                    try:
                        self.delete_record(system_identity, draft_id, {})
                    except Exception:
                        pass  # don't let rollback errors mask the original

        with ThreadPoolExecutor(max_workers=min(_BULK_WORKERS, len(draft_ids))) as pool:
            list(pool.map(delete_one, draft_ids))
