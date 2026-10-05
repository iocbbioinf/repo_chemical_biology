"""Model for metabolomics dataset.

This package contains the model definition for Metabolomics dataset (GC-MS / LC-MS, vendor raw files).
To change model's metadata, edit the metadata.yaml file. Metadata shared
with other mass spectra models live in models/common/mass_spec.yaml.
"""

from __future__ import annotations

from .model import metabolomics_dataset_model

__all__ = ("metabolomics_dataset_model",)
