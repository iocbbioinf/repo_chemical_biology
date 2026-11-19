"""
Dataset
"""
from __future__ import annotations

from invenio_i18n import lazy_gettext as _
from oarepo_model.api import model
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_model.customizations import AddFacetGroup, AddToDictionary
from oarepo_model.datatypes.registry import from_yaml
from ccmm_invenio.models import ccmm_production_preset_1_1_0

# TODO: Consider letting users add an image/icon for the model,
# so that the deposit model selection page is more visually appealing.
dataset_model = model(
    "dataset",
    version="1.0.0",
    description="Dataset",
    presets=[

        ccmm_production_preset_1_1_0

    ],
    types=[
        from_yaml("metadata.yaml", __file__)
    ],
    metadata_type="Metadata",
    customizations=[
        # Add your customizations here, such as custom exports and class mixins. 
        # The list of available extensions is at https://github.com/oarepo/oarepo-model.
        # If you do not find a customization that suits your needs or need a
        # help with using customizations, please contact us at support@cesnet.cz and
        # specify the keyword "Invenio repository development" inside the subject or
        # mail body of the request.

        # Facet for keywords. The generated "metadata.subjects" facet aggregates
        # on subjects.id, so it only counts vocabulary subjects; free-text
        # keywords are stored as {"subject": "..."} without an id.
        AddToDictionary(
            "RecordFacets",
            {
                "metadata.subjects.subject": TermsFacet(
                    field="metadata.subjects.subject",
                    label=_("Keywords"),
                ),
            },
        ),

        # Facets shown on the search page. Without a facet group all ~200
        # generated facets (incl. deeply nested CCMM fields) would be shown.
        AddFacetGroup(
            "default",
            [
                # domain-specific fields (metadata.yaml)
                "metadata.domain_type",
                "metadata.sample_type",
                "metadata.analysis_type",
                "metadata.tissue_type",
                "metadata.microbiology.species",
                "metadata.plant_biology.species",
                # general fields (CCMM / RDM preset)
                "metadata.resource_type",
                "metadata.subjects",
                "metadata.subjects.subject",
                "metadata.languages",
                "metadata.publication_date",
                "metadata.creators.affiliations",
                "metadata.rights",
                "access_status",
            ],
        ),
    ],
    configuration={
        "ui_blueprint_name": "dataset_ui"
    }
)
