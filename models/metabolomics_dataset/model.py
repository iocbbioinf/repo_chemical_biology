"""
Metabolomics dataset
"""
from __future__ import annotations

from invenio_i18n import lazy_gettext as _
from oarepo_model.api import model
from oarepo_model.customizations import AddMetadataExport
from oarepo_model.datatypes.registry import from_yaml
from ccmm_invenio.models import ccmm_production_preset_1_1_0

from .serializers import DataCiteJSONSerializer

metabolomics_dataset_model = model(
    "metabolomics_dataset",
    version="1.0.0",
    description="Metabolomics dataset (GC-MS / LC-MS, vendor raw files)",
    presets=[
        ccmm_production_preset_1_1_0
    ],
    types=[
        from_yaml("../common/mass_spec.yaml", __file__),
        from_yaml("metadata.yaml", __file__),
    ],
    metadata_type="Metadata",
    customizations=[
        # export for datacite
        AddMetadataExport(
            code="datacite",
            name=_("Datacite export"),
            mimetype="application/vnd.datacite.datacite+json",
            serializer=DataCiteJSONSerializer()
        ),
    ],
    configuration={
        "ui_blueprint_name": "metabolomics_dataset_ui"
    }
)
