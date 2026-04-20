"""MSRun record — one mzML file's metadata (instrument, software, samples, run, chromatograms).

Individual spectra are stored as separate Spectrum records referencing this MSRun.
"""

from __future__ import annotations

from .model import msrun_model

__all__ = ("msrun_model",)
