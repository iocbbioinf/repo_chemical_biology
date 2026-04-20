"""MSRun record — metadata for one mzML file within a Dataset."""

from __future__ import annotations

from invenio_i18n import lazy_gettext as _
from invenio_records_permissions.generators import AuthenticatedUser
from oarepo_model.api import model
from oarepo_model.customizations import PrependMixin, AddMetadataExport
from oarepo_model.customizations.high_level.index_mapping import PatchIndexPropertyMapping
from oarepo_model.model import ModelMixin
from oarepo_model.datatypes.registry import from_yaml
from ccmm_invenio.models import ccmm_production_preset_1_1_0

from .pids import MSRunNoDOIServiceConfigMixin
from .serializers import DataCiteJSONSerializer


class MSRunPermissionPolicyMixin(ModelMixin):
    can_view_deposit_page = [AuthenticatedUser()]


msrun_model = model(
    "msrun",
    version="1.0.0",
    description="MS Run — metadata for one mzML file",
    presets=[
        ccmm_production_preset_1_1_0
    ],
    types=[
        from_yaml("metadata.yaml", __file__)
    ],
    metadata_type="Metadata",
    customizations=[
        PrependMixin("PermissionPolicy", MSRunPermissionPolicyMixin),
        PrependMixin("RecordServiceConfig", MSRunNoDOIServiceConfigMixin),

        # Disable fulltext indexing on large nested structures that don't need
        # free-text search — they balloon the boolean clause count past OS limits.
        PatchIndexPropertyMapping("metadata.cv_list",                  {"type": "object", "enabled": False}),
        PatchIndexPropertyMapping("metadata.file_content",             {"type": "object", "enabled": False}),
        PatchIndexPropertyMapping("metadata.source_files",             {"type": "object", "enabled": False}),
        PatchIndexPropertyMapping("metadata.contacts",                 {"type": "object", "enabled": False}),
        PatchIndexPropertyMapping("metadata.referenceable_param_groups", {"type": "object", "enabled": False}),
        PatchIndexPropertyMapping("metadata.samples",                  {"type": "object", "enabled": False}),
        PatchIndexPropertyMapping("metadata.software_list",            {"type": "object", "enabled": False}),
        PatchIndexPropertyMapping("metadata.scan_settings_list",       {"type": "object", "enabled": False}),
        PatchIndexPropertyMapping("metadata.instrument_configurations",{"type": "object", "enabled": False}),
        PatchIndexPropertyMapping("metadata.data_processing_list",     {"type": "object", "enabled": False}),
        PatchIndexPropertyMapping("metadata.run_cv_params",            {"type": "object", "enabled": False}),
        PatchIndexPropertyMapping("metadata.chromatogram_list",        {"type": "object", "enabled": False}),

        AddMetadataExport(
            code="datacite",
            name=_("Datacite export"),
            mimetype="application/vnd.datacite.datacite+json",
            serializer=DataCiteJSONSerializer()
        ),
    ],
    configuration={}
)
