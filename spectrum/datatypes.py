import marshmallow as ma
from oarepo_model.datatypes.base import DataType


class VectorMarshmallowField(ma.fields.List):
    """A list of floats representing a vector/embedding."""

    def __init__(self, *args, **kwargs):
        super().__init__(ma.fields.Float(), *args, **kwargs)


class VectorDataType(DataType):
    TYPE = "vector"
    marshmallow_field_class = VectorMarshmallowField
    jsonschema_type = {"type": "array", "items": {"type": "number"}}

    def create_mapping(self, element):
        dims = element.get("dims", 1536)
        # dense_vector for Elasticsearch 8 / OpenSearch knn_vector
        return {
            "type": "knn_vector",
            "dimension": dims,
        }

    def create_json_schema(self, element):
        return {
            "type": "array",
            "items": {"type": "number"},
        }


DATATYPES = {
    "vector": VectorDataType,
}
