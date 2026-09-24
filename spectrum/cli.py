"""CLI for Universal Spectrum Identifier maintenance: ``invenio usi ...``."""

import click
from flask.cli import with_appcontext


@click.group()
def usi():
    """Universal Spectrum Identifier (USI) commands."""


@usi.command("refresh")
@click.argument("dataset_id")
@with_appcontext
def refresh(dataset_id):
    """Recompute USIs of all published spectra of DATASET_ID.

    Run after setting the dataset's usi_collection (PXD/MSV accession) to
    replace the USI000000 placeholder.
    """
    from .usi import refresh_dataset_usis

    changed = refresh_dataset_usis(dataset_id)
    click.echo(f"Updated USI of {changed} spectrum record(s) in dataset {dataset_id}.")
