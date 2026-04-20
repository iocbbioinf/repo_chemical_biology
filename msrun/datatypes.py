"""PID field helpers for MSRun pid-relations."""

from __future__ import annotations

from typing import Any


def dataset_pid_field(element: dict[str, Any]) -> Any:
    """Return the PID field for the parent Dataset record."""
    from dataset import dataset_model  # noqa: PLC0415

    return dataset_model.Record.pid
