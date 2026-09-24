from ccmm_invenio.serializers.production.datacite import ProductionDataCiteSchema
from flask_resources import BaseListSchema, MarshmallowSerializer
from flask_resources.serializers import JSONSerializer
from marshmallow import missing

# DataCite identifierType for each USI collection prefix. RPXD/RMSV are
# reprocessed datasets, i.e. not the same resource, so they are not exported.
USI_COLLECTION_IDENTIFIER_TYPES = {
    "PXD": "ProteomeXchange",
    "PXL": "ProteomeXchange",
    "MSV": "MassIVE",
}


class DatasetDataCiteSchema(ProductionDataCiteSchema):
    """Adds the USI collection accession (PXD/MSV) as an alternate identifier."""

    def get_identifiers(self, obj):
        identifiers = super().get_identifiers(obj)
        identifiers = [] if identifiers is missing else identifiers

        accession = obj.get("metadata", {}).get("usi_collection")
        identifier_type = USI_COLLECTION_IDENTIFIER_TYPES.get((accession or "")[:3])
        if identifier_type:
            identifiers.append({"identifier": accession, "identifierType": identifier_type})
        return identifiers or missing


class DataCiteJSONSerializer(MarshmallowSerializer):
    """DataCite JSON serializer for datasets (CCMM production schema + USI collection)."""

    def __init__(self, **options):
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=DatasetDataCiteSchema,
            list_schema_cls=BaseListSchema,
            schema_kwargs={},
            **options,
        )
