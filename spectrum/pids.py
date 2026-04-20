"""Disable DOI PID for spectrum records — only internal recid + OAI are used."""

from oarepo_model.model import ModelMixin


class SpectrumNoDOIServiceConfigMixin(ModelMixin):
    """Strip 'doi' from PID providers and required PIDs for this model."""

    @property
    def pids_providers(self):
        return {k: v for k, v in super().pids_providers.items() if k != "doi"}

    @property
    def pids_required(self):
        return [s for s in super().pids_required if s != "doi"]
