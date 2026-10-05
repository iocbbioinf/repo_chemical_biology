"""Model for proteomics dataset.

This package contains the model definition for Proteomics dataset (LC-MS/MS, mzML files).
To change model's metadata, edit the metadata.yaml file. Metadata shared
with other mass spectra models live in models/common/mass_spec.yaml.
"""

from __future__ import annotations

from .model import proteomics_dataset_model

__all__ = ("proteomics_dataset_model",)
