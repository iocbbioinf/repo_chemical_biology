"""Compute and store the Universal Spectrum Identifier (metadata.usi) of spectra.

The USI is assembled from the parent records:

    collection  <- Dataset  metadata.usi_collection (placeholder USI000000 if empty)
    msRun       <- MSRun    metadata.usi_run_name, else the default source file name
    index       <- Spectrum metadata.native_id

See common/usi.py for the string format.
"""

from __future__ import annotations

from invenio_db import db
from invenio_drafts_resources.services.records.components import ServiceComponent
from invenio_pidstore.errors import PersistentIdentifierError

from common.usi import ms_run_name, spectrum_usi


def _resolve(record_cls, ref):
    """Return the published record referenced by a pid-relation value, or None."""
    pid_value = (ref or {}).get("id")
    if not pid_value:
        return None
    try:
        return record_cls.pid.resolve(pid_value)
    except PersistentIdentifierError:
        return None


def msrun_usi_name(msrun_metadata):
    """msRun component for an MSRun record: explicit name, else its default source file."""
    if msrun_metadata.get("usi_run_name"):
        return msrun_metadata["usi_run_name"]

    source_files = msrun_metadata.get("source_files") or []
    default_ref = msrun_metadata.get("default_source_file_ref")
    for source_file in source_files:
        if default_ref and source_file.get("source_file_id") == default_ref:
            return ms_run_name(source_file.get("name"))
    if len(source_files) == 1:
        return ms_run_name(source_files[0].get("name"))
    return None


def compute_spectrum_usi(metadata):
    """Return the USI for spectrum metadata, or None if it cannot be determined."""
    from dataset.model import DatasetRecord
    from msrun.model import MSRunRecord

    msrun = _resolve(MSRunRecord, metadata.get("msrun"))
    if msrun is None:
        return None
    dataset = _resolve(DatasetRecord, metadata.get("dataset"))
    collection = (dataset or {}).get("metadata", {}).get("usi_collection")

    return spectrum_usi(collection, msrun_usi_name(msrun.get("metadata", {})), metadata.get("native_id"))


def set_spectrum_usi(record):
    """Overwrite record.metadata.usi with the computed value (removing it if unknown)."""
    metadata = record.get("metadata")
    if metadata is None:
        return
    usi = compute_spectrum_usi(metadata)
    if usi:
        metadata["usi"] = usi
    else:
        metadata.pop("usi", None)


class SpectrumUSIComponent(ServiceComponent):
    """Keeps metadata.usi in sync on drafts and on publish; client-supplied values are ignored."""

    def create(self, identity, data=None, record=None, errors=None, **kwargs):
        set_spectrum_usi(record)

    def update(self, identity, data=None, record=None, **kwargs):
        set_spectrum_usi(record)

    def update_draft(self, identity, data=None, record=None, errors=None, **kwargs):
        set_spectrum_usi(record)

    def publish(self, identity, draft=None, record=None, **kwargs):
        # Recompute: the dataset may have received its accession since the draft was saved.
        set_spectrum_usi(record)


def refresh_dataset_usis(dataset_id):
    """Recompute metadata.usi of all published spectra of a dataset.

    Run after a dataset's usi_collection is set or changed, so USI000000
    placeholders are replaced. Drafts are skipped: they are recomputed on publish.
    Returns the number of records whose USI changed.
    """
    from invenio_access.permissions import system_identity

    from .model import spectrum_model

    service = spectrum_model.proxies.current_service
    record_cls = service.record_cls

    hits = service.scan(system_identity, params={"q": f'metadata.dataset.id:"{dataset_id}"'})
    record_ids = [hit["id"] for hit in hits]

    changed = []
    for record_id in record_ids:
        record = record_cls.pid.resolve(record_id)
        old = record["metadata"].get("usi")
        set_spectrum_usi(record)
        if record["metadata"].get("usi") != old:
            # refresh the denormalized relation keys (usi_collection, usi_run_name) as well
            record.relations.dereference()
            record.commit()
            changed.append(record)
    db.session.commit()

    for record in changed:
        service.indexer.index(record)
    return len(changed)
