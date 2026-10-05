"""File format validation for mass spectra models.

Each mass spectra model accepts only its own data format plus a few
auxiliary (documentation / sample sheet) formats:

* proteomics_dataset - open mzML files,
* metabolomics_dataset - vendor binary raw files; the extension must match
  the ``metadata.metabolomics.raw_format`` selected in the record.

Two checks are done:

* on upload (draft file service, ``init_files``) - the file extension must be
  one of the allowed ones,
* on publish (record service) - at least one data file in the expected format
  must be present.
"""

from __future__ import annotations

from typing import Any, ClassVar

from invenio_drafts_resources.services.records.components import ServiceComponent
from invenio_i18n import gettext as _
from invenio_records_resources.services.files.components import FileServiceComponent
from invenio_records_resources.services.files.config import FileServiceConfig
from marshmallow import ValidationError

# Documentation, sample sheets and processed results that may accompany the data.
AUXILIARY_EXTENSIONS = (".txt", ".md", ".pdf", ".csv", ".tsv", ".xlsx", ".json")

MZML_EXTENSIONS = (".mzml", ".mzml.gz")

# Vendor formats that are directories on disk (Bruker/Agilent .d, Waters .raw)
# must be uploaded zipped.
RAW_FORMAT_EXTENSIONS: dict[str, tuple[str, ...]] = {
    "thermo_raw": (".raw",),
    "bruker_d": (".d.zip",),
    "waters_raw": (".raw.zip",),
    "sciex_wiff": (".wiff", ".wiff2", ".wiff.scan"),
    "agilent_d": (".d.zip",),
    "shimadzu_lcd": (".lcd", ".qgd"),
    "andi_cdf": (".cdf",),
}
RAW_EXTENSIONS = tuple(sorted({ext for exts in RAW_FORMAT_EXTENSIONS.values() for ext in exts}))


def has_extension(key: str, extensions: tuple[str, ...]) -> bool:
    """Return True if the file name ends with one of the extensions (case insensitive)."""
    return key.lower().endswith(extensions)


class FileExtensionComponent(FileServiceComponent):
    """Reject uploads of files whose extension the model does not accept."""

    data_extensions: ClassVar[tuple[str, ...]] = ()

    def init_files(self, identity: Any, id_: str, record: Any, data: list[dict]) -> None:
        """Check extensions of the files being initialized."""
        allowed = self.data_extensions + AUXILIARY_EXTENSIONS
        rejected = [f["key"] for f in data if not has_extension(f["key"], allowed)]
        if rejected:
            raise ValidationError(
                _("Unsupported file type: %(files)s. Allowed extensions: %(allowed)s.")
                % {"files": ", ".join(rejected), "allowed": ", ".join(allowed)},
                field_name="files",
            )


class MzMLFileExtensionComponent(FileExtensionComponent):
    """Upload check for proteomics datasets."""

    data_extensions = MZML_EXTENSIONS


class RawFileExtensionComponent(FileExtensionComponent):
    """Upload check for metabolomics datasets."""

    data_extensions = RAW_EXTENSIONS


class RequiredDataFilesComponent(ServiceComponent):
    """On publish, require at least one data file in the expected format."""

    def expected_extensions(self, draft: Any) -> tuple[str, ...]:
        """Return the extensions of the data files expected in the draft."""
        raise NotImplementedError

    def publish(self, identity: Any, draft: Any = None, record: Any = None) -> None:
        """Check that the draft contains a data file."""
        expected = self.expected_extensions(draft)
        keys = list(draft.files.entries.keys()) if draft.files.enabled else []
        if not any(has_extension(key, expected) for key in keys):
            raise ValidationError(
                _("The dataset must contain at least one data file (%(expected)s).")
                % {"expected": ", ".join(expected)},
                field_name="files",
            )


class RequiredMzMLFilesComponent(RequiredDataFilesComponent):
    """Publish check for proteomics datasets."""

    def expected_extensions(self, draft: Any) -> tuple[str, ...]:
        return MZML_EXTENSIONS


class RequiredRawFilesComponent(RequiredDataFilesComponent):
    """Publish check for metabolomics datasets - files must match the selected raw format."""

    def expected_extensions(self, draft: Any) -> tuple[str, ...]:
        raw_format = draft.metadata.get("metabolomics", {}).get("raw_format")
        return RAW_FORMAT_EXTENSIONS.get(raw_format, RAW_EXTENSIONS)


def draft_file_service_mixin(component: type[FileExtensionComponent]) -> type:
    """Create a mixin for DraftFileServiceConfig adding the upload check."""
    return type(
        f"{component.__name__}ServiceConfigMixin",
        (),
        {"components": [*FileServiceConfig.components, component]},
    )
