from __future__ import annotations

from typing import Any

import marshmallow as ma
from oarepo_model.datatypes.base import DataType


def dataset_pid_field(element: dict[str, Any]) -> Any:
    """Return the PID field context for the dataset record.

    Used as pid_field in the spectrum metadata.yaml pid-relation for the
    back-reference to the parent dataset.  Imported lazily to avoid circular
    imports during app initialisation.
    """
    from dataset import dataset_model  # noqa: PLC0415

    return dataset_model.Record.pid


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
