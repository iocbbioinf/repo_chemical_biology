"""Universal Spectrum Identifier (USI) helpers.

Specification: https://www.psidev.info/usi (USI 1.0), collection identifiers:
https://github.com/HUPO-PSI/usi/blob/master/CollectionIdentifiers.md

    mzspec:<collection>:<msRun>:<indexType>:<indexNumber>[:<interpretation>]

This module has no Invenio dependencies so it can be unit-tested on its own.
"""

from __future__ import annotations

import posixpath
import re

USI_PREFIX = "mzspec"

# Placeholder for a dataset that has no public collection identifier yet.
# The spec requires it to be search-and-replaced once the dataset is registered.
USI_PLACEHOLDER_COLLECTION = "USI000000"

# Permitted collection identifiers (CollectionIdentifiers.md). USI000000 is
# intentionally not accepted as a stored value — it is only a fallback.
COLLECTION_PATTERN = r"^(PXD\d{6}|RPXD\d{6}|PXL\d{6}|MSV\d{9}|RMSV\d{9})$"

INDEX_TYPES = ("scan", "index", "nativeId", "trace")

# The msRun name may contain colons, so anchor on the limited indexType values
# (spec 3.3.4) instead of splitting on ':'.
USI_RE = re.compile(
    r"^mzspec:(?P<collection>[^:]+):(?P<ms_run>.+?)"
    r":(?P<index_type>scan|index|nativeId|trace):(?P<index>[^:]+)"
    r"(?::(?P<interpretation>.+))?$"
)

_NATIVE_ID_PAIR_RE = re.compile(r"(\S+?)=(\S+)")


class InvalidUSI(ValueError):
    """The string is not a valid USI."""


def ms_run_name(file_name: str | None) -> str | None:
    """Return the msRun component for a file name: the root name, no path or extension."""
    if not file_name:
        return None
    base = posixpath.basename(file_name.replace("\\", "/").rstrip("/"))
    root, _ext = posixpath.splitext(base)
    return root or None


def index_from_native_id(native_id: str | None) -> tuple[str, str] | None:
    """Translate an mzML nativeID into the USI (indexType, indexNumber) pair.

    - ``scan=N`` (scan number only nativeID format)           -> scan:N
    - Thermo ``controllerType=0 controllerNumber=1 scan=N``   -> scan:N
    - ``index=N`` (multiple peak list nativeID format)         -> index:N
    - any other all-integer ``key=value`` nativeID (SCIEX, Waters, Bruker,
      non-MS Thermo controllers) -> nativeId:v1,v2,... in nativeID key order

    Returns None if the nativeID cannot be expressed as a USI index.
    """
    if not native_id:
        return None
    pairs = _NATIVE_ID_PAIR_RE.findall(native_id.strip())
    if not pairs or not all(v.isdigit() for _, v in pairs):
        return None
    keys = [k for k, _ in pairs]
    values = [v for _, v in pairs]

    if keys == ["scan"]:
        return "scan", values[0]
    if keys == ["index"]:
        return "index", values[0]
    if keys == ["controllerType", "controllerNumber", "scan"] and values[:2] == ["0", "1"]:
        return "scan", values[2]
    return "nativeId", ",".join(values)


def build_usi(
    collection: str | None,
    ms_run: str,
    index_type: str,
    index: str | int,
    interpretation: str | None = None,
) -> str:
    """Assemble a USI string. An empty collection becomes the USI000000 placeholder."""
    if index_type not in INDEX_TYPES:
        raise InvalidUSI(f"Invalid indexType '{index_type}'")
    if not ms_run:
        raise InvalidUSI("msRun component is required")
    usi = f"{USI_PREFIX}:{collection or USI_PLACEHOLDER_COLLECTION}:{ms_run}:{index_type}:{index}"
    return f"{usi}:{interpretation}" if interpretation else usi


def spectrum_usi(collection: str | None, ms_run: str | None, native_id: str | None) -> str | None:
    """Build the USI for a spectrum, or None if the run name or nativeID are unusable."""
    index = index_from_native_id(native_id)
    if not ms_run or index is None:
        return None
    return build_usi(collection, ms_run, *index)


def parse_usi(usi: str) -> dict[str, str | None]:
    """Split a USI into its components; raises InvalidUSI."""
    m = USI_RE.match(usi.strip()) if usi else None
    if not m:
        raise InvalidUSI(f"Invalid USI: {usi!r}")
    return m.groupdict()


def is_placeholder(usi: str) -> bool:
    """True if the USI uses the USI000000 placeholder collection."""
    return parse_usi(usi)["collection"] == USI_PLACEHOLDER_COLLECTION
