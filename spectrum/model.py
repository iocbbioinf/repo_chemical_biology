"""
A mass spectrum record
"""
from __future__ import annotations

from invenio_i18n import lazy_gettext as _
from invenio_records_permissions.generators import AuthenticatedUser
from oarepo_model.api import model
from oarepo_model.customizations import PrependMixin, AddMetadataExport
from oarepo_model.customizations.patch_json_file import PatchJSONFile
from oarepo_model.customizations.high_level.index_mapping import PatchIndexPropertyMapping
from oarepo_model.model import ModelMixin
from oarepo_model.presets.drafts import drafts_preset
from oarepo_model.presets.records_resources import records_resources_preset
from oarepo_model.presets.ui_links import ui_links_preset
from oarepo_model.datatypes.registry import from_yaml
from oarepo_rdm.model.presets import rdm_complete_preset

from .datatypes import DATATYPES
from .pids import SpectrumNoDOIServiceConfigMixin
from .serializers import DataCiteJSONSerializer
from .bulk import BulkCreateResourceMixin, BulkCreateServiceMixin
from .similarity import SimilaritySearchResourceMixin, SimilaritySearchServiceMixin

class SpectrumSearchConfigMixin(ModelMixin):
    sort_options = {
        "bestmatch": dict(title=_("Best match"), fields=["_score"]),
        "newest":    dict(title=_("Newest"),     fields=["-created"]),
        "oldest":    dict(title=_("Oldest"),     fields=["created"]),
        "native_id":       dict(title=_("Scan ID"),        fields=["metadata.native_id"]),
        "native_id_desc":  dict(title=_("Scan ID (desc)"), fields=["-metadata.native_id"]),
        "precmz":          dict(title=_("Precursor m/z"),        fields=["metadata.precursor_list.selected_ions.selected_ion_mz"]),
        "precmz_desc":     dict(title=_("Precursor m/z (desc)"), fields=["-metadata.precursor_list.selected_ions.selected_ion_mz"]),
        "charge":          dict(title=_("Charge"),        fields=["metadata.precursor_list.selected_ions.charge_state"]),
        "charge_desc":     dict(title=_("Charge (desc)"), fields=["-metadata.precursor_list.selected_ions.charge_state"]),
        "polarity":        dict(title=_("Mode"),           fields=["metadata.scan_polarity.id"]),
        "polarity_desc":   dict(title=_("Mode (desc)"),    fields=["-metadata.scan_polarity.id"]),
        "frag_method":     dict(title=_("Fragmentation"),       fields=["metadata.precursor_list.activation.dissociation_method.id"]),
        "frag_method_desc":dict(title=_("Fragmentation (desc)"),fields=["-metadata.precursor_list.activation.dissociation_method.id"]),
        "run_id":          dict(title=_("Run ID"),         fields=["metadata.msrun.metadata.run_id"]),
        "run_id_desc":     dict(title=_("Run ID (desc)"),  fields=["-metadata.msrun.metadata.run_id"]),
        "dataset":         dict(title=_("Dataset"),        fields=["metadata.dataset.metadata.title"]),
        "dataset_desc":    dict(title=_("Dataset (desc)"), fields=["-metadata.dataset.metadata.title"]),
        "ms_level":        dict(title=_("MS level"),       fields=["metadata.ms_level"]),
        "ms_level_desc":   dict(title=_("MS level (desc)"),fields=["-metadata.ms_level"]),
        "instrument_model":      dict(title=_("Instrument"),       fields=["metadata.instrument_model"]),
        "instrument_model_desc": dict(title=_("Instrument (desc)"),fields=["-metadata.instrument_model"]),
    }


class SpectrumPermissionPolicyMixin(ModelMixin):
    """Custom permission policy for spectrum."""

    can_view_deposit_page = [AuthenticatedUser()]


# TODO: Consider letting users add an image/icon for the model,
# so that the deposit model selection page is more visually appealing.
spectrum_model = model(
    "spectrum",
    version="1.0.0",
    description="A mass spectrum record",
    presets=[

        rdm_complete_preset

    ],
    types=[
        DATATYPES,
        from_yaml("metadata.yaml", __file__),
    ],
    metadata_type="Metadata",
    customizations=[
        # Add your customizations here, such as custom exports and class mixins. 
        # The list of available extensions is at https://github.com/oarepo/oarepo-model.
        # If you do not find a customization that suits your needs or need a
        # help with using customizations, please contact us at support@cesnet.cz and
        # specify the keyword "Invenio repository development" inside the subject or
        # mail body of the request.
        # TODO: remove this customization if you use oarepo-communities for RDM 14
        PrependMixin("PermissionPolicy", SpectrumPermissionPolicyMixin),
        PrependMixin("RecordServiceConfig", SpectrumNoDOIServiceConfigMixin),
        PrependMixin("RecordSearchOptions", SpectrumSearchConfigMixin),
        PrependMixin("DraftSearchOptions", SpectrumSearchConfigMixin),
        PrependMixin("RecordResource", BulkCreateResourceMixin),
        PrependMixin("RecordResource", SimilaritySearchResourceMixin),
        PrependMixin("RecordService", BulkCreateServiceMixin),
        PrependMixin("RecordService", SimilaritySearchServiceMixin),
        PatchJSONFile("record-mapping", {"settings": {"index": {"knn": True}}}),
        PatchJSONFile("draft-mapping", {"settings": {"index": {"knn": True}}}),
        # Exclude binary spectral data from OpenSearch indexing.
        # The data is stored in PostgreSQL (_source) and returned by the API,
        # but "enabled: false" prevents OpenSearch from parsing, indexing or
        # building doc_values for anything inside binary_data_array_list.
        PatchIndexPropertyMapping(
            "metadata.binary_data_array_list",
            {"type": "object", "enabled": False},
        ),

        # export for datacite
        AddMetadataExport(
            code="datacite",
            name=_("Datacite export"),
            mimetype="application/vnd.datacite.datacite+json",
            serializer=DataCiteJSONSerializer()
        ),
    ],
    configuration={
        "ui_blueprint_name": "spectrum_ui"
    }
)
