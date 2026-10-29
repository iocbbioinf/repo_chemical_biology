"""Generate vocabulary fixtures from established ontologies.

Writes fixtures/edam-topics.yaml, fixtures/ncbitaxon.yaml and fixtures/unimod.yaml.
Sources are downloaded from the ontology providers:

* EDAM topics - https://edamontology.org/EDAM.tsv (curated subset, EDAM_TOPICS)
* NCBI Taxonomy - NCBI E-utilities (curated subset, NCBI_TAXA)
* UNIMOD - https://www.unimod.org/obo/unimod.obo (all modifications)

Usage: python scripts/build_ontology_fixtures.py
"""

from __future__ import annotations

import csv
import io
import json
import re
import urllib.request
from pathlib import Path

import yaml

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"

# Dataset domain types (EDAM topics), title is the EDAM preferred label
# unless overridden here.
EDAM_TOPICS = {
    "topic_0121": None,  # Proteomics
    "topic_3172": None,  # Metabolomics
    "topic_0153": "Lipidomics",  # EDAM label "Lipids", Lipidomics is its synonym
    "topic_3922": None,  # Proteogenomics
    "topic_3955": None,  # Fluxomics
    "topic_3308": None,  # Transcriptomics
    "topic_0622": None,  # Genomics
    "topic_3174": None,  # Metagenomics
}

# Commonly studied organisms. More can be added here or through the vocabulary UI.
NCBI_TAXA = [
    # animals
    9606, 10090, 10116, 9913, 9823, 9031, 7955, 7227, 6239, 8355,
    # fungi
    4932, 559292, 4896, 5476, 5061, 162425,
    # bacteria
    562, 83333, 1423, 287, 1280, 1773, 28901, 573, 1902, 1148, 1590, 1351, 1313, 210, 1718,
    # plants and algae
    3702, 4530, 4577, 4081, 4113, 4565, 4513, 3708, 3847, 3880, 3218, 3055, 4097, 4100, 29760, 3694,
]


def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=120) as response:  # noqa: S310 - fixed https urls
        return response.read().decode("utf-8")


def dump(path: Path, items: list[dict]) -> None:
    with path.open("w") as f:
        yaml.safe_dump_all(items, f, allow_unicode=True, sort_keys=False, width=100)
    print(f"{path}: {len(items)} items")


def edam_topics() -> list[dict]:
    rows = csv.DictReader(io.StringIO(fetch("https://edamontology.org/EDAM.tsv")), delimiter="\t")
    by_id = {row["Class ID"].rsplit("/", 1)[-1]: row for row in rows}
    items = []
    for topic_id, title in EDAM_TOPICS.items():
        row = by_id[topic_id]
        items.append(
            {
                "id": topic_id,
                "title": {"en": title or row["Preferred Label"]},
                "props": {"iri": row["Class ID"]},
            }
        )
    return items


def ncbi_taxa() -> list[dict]:
    ids = ",".join(str(i) for i in NCBI_TAXA)
    result = json.loads(
        fetch(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=taxonomy&id={ids}&retmode=json")
    )["result"]
    items = []
    for uid in result["uids"]:
        taxon = result[uid]
        props = {
            "iri": f"http://purl.obolibrary.org/obo/NCBITaxon_{uid}",
            "rank": taxon["rank"],
        }
        if taxon["commonname"]:
            props["common_name"] = taxon["commonname"]
        items.append({"id": f"NCBITaxon:{uid}", "title": {"en": taxon["scientificname"]}, "props": props})
    return items


def unimod() -> list[dict]:
    items = []
    for term in fetch("https://www.unimod.org/obo/unimod.obo").split("\n[Term]\n")[1:]:
        fields = dict(line.split(": ", 1) for line in term.splitlines() if ": " in line)
        accession = fields["id"]
        if accession == "UNIMOD:0" or fields.get("is_obsolete") == "true":
            continue
        name = fields["name"]
        # def: "Phosphorylation." [references]
        match = re.match(r'"(.*?)\.?"\s*\[', fields.get("def", ""))
        full_name = re.sub(r"\\(.)", r"\1", match.group(1)) if match else ""  # OBO escapes, e.g. \'
        number = accession.split(":", 1)[1]
        items.append(
            {
                "id": accession,
                # search works on the title, so include both the full name and PSI-MS name
                "title": {"en": f"{full_name} ({name})" if full_name and full_name != name else name},
                "props": {
                    "psi_ms_name": name,
                    "iri": f"https://www.unimod.org/modifications_view.php?editid1={number}",
                },
            }
        )
    return items


if __name__ == "__main__":
    dump(FIXTURES / "edam-topics.yaml", edam_topics())
    dump(FIXTURES / "ncbitaxon.yaml", ncbi_taxa())
    dump(FIXTURES / "unimod.yaml", unimod())
