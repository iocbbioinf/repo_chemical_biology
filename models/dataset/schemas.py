"""Marshmallow schemas used by the dataset model (see metadata.yaml)."""

from __future__ import annotations

from invenio_rdm_records.services.schemas.metadata import FeatureSchema, LocationSchema
from marshmallow import ValidationError, fields, validates_schema


class DatasetLocationSchema(LocationSchema):
    """RDM location that also checks the latitude/longitude range of a point."""

    @validates_schema
    def validate_point(self, data, **kwargs):
        """Validate point coordinates, GeoJSON order is [longitude, latitude]."""
        coordinates = (data.get("geometry") or {}).get("coordinates")
        # only points have a flat list of numbers as coordinates
        if not (isinstance(coordinates, list) and len(coordinates) == 2
                and all(isinstance(c, (int, float)) for c in coordinates)):
            return
        longitude, latitude = coordinates
        if not -90 <= latitude <= 90:
            raise ValidationError("Latitude must be between -90 and 90.", field_name="geometry")
        if not -180 <= longitude <= 180:
            raise ValidationError("Longitude must be between -180 and 180.", field_name="geometry")


class DatasetFeatureSchema(FeatureSchema):
    """Geolocations (metadata.locations) of a dataset."""

    features = fields.List(fields.Nested(DatasetLocationSchema))
