"""Unit tests for common/usi.py (no Invenio app needed)."""

import re

import pytest

from common.usi import (
    COLLECTION_PATTERN,
    InvalidUSI,
    build_usi,
    index_from_native_id,
    is_placeholder,
    ms_run_name,
    parse_usi,
    spectrum_usi,
)


@pytest.mark.parametrize(
    "native_id, expected",
    [
        ("scan=17555", ("scan", "17555")),
        ("controllerType=0 controllerNumber=1 scan=43920", ("scan", "43920")),
        ("controllerType=5 controllerNumber=1 scan=7", ("nativeId", "5,1,7")),
        ("sample=1 period=1 cycle=2740 experiment=10", ("nativeId", "1,1,2740,10")),
        ("function=10 process=1 scan=345", ("nativeId", "10,1,345")),
        ("frame=120 scan=475", ("nativeId", "120,475")),
        ("index=12", ("index", "12")),
        ("file=foo.mgf", None),
        ("", None),
        (None, None),
    ],
)
def test_index_from_native_id(native_id, expected):
    assert index_from_native_id(native_id) == expected


@pytest.mark.parametrize(
    "file_name, expected",
    [
        ("Adult_Frontalcortex_bRP_Elite_85_f09.raw", "Adult_Frontalcortex_bRP_Elite_85_f09"),
        ("C:\\data\\run01.RAW", "run01"),
        ("/data/sample.d/", "sample"),
        ("run02.mzML", "run02"),
        (None, None),
    ],
)
def test_ms_run_name(file_name, expected):
    assert ms_run_name(file_name) == expected


def test_spectrum_usi_uses_placeholder_without_collection():
    assert spectrum_usi(None, "example", "scan=1") == "mzspec:USI000000:example:scan:1"


def test_spectrum_usi_with_collection():
    assert (
        spectrum_usi("PXD000561", "Adult_Frontalcortex_bRP_Elite_85_f09", "scan=17555")
        == "mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555"
    )


def test_spectrum_usi_unknown_parts():
    assert spectrum_usi("PXD000561", None, "scan=1") is None
    assert spectrum_usi("PXD000561", "run", "garbage") is None


def test_build_with_interpretation_and_parse_roundtrip():
    usi = build_usi("PXD000561", "Adult_Frontalcortex_bRP_Elite_85_f09", "scan", 17555, "VLHPLEGAVVIIFK/2")
    assert usi == "mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555:VLHPLEGAVVIIFK/2"
    assert parse_usi(usi) == {
        "collection": "PXD000561",
        "ms_run": "Adult_Frontalcortex_bRP_Elite_85_f09",
        "index_type": "scan",
        "index": "17555",
        "interpretation": "VLHPLEGAVVIIFK/2",
    }


def test_parse_ms_run_with_colon():
    parsed = parse_usi("mzspec:PXD000001:weird:name:scan:5")
    assert parsed["ms_run"] == "weird:name"
    assert parsed["index"] == "5"


@pytest.mark.parametrize("bad", ["", "mzspec:PXD000001", "foo:PXD000001:run:scan:1", "mzspec:PXD000001:run:bogus:1"])
def test_parse_invalid(bad):
    with pytest.raises(InvalidUSI):
        parse_usi(bad)


def test_build_invalid_index_type():
    with pytest.raises(InvalidUSI):
        build_usi("PXD000001", "run", "bogus", 1)


def test_is_placeholder():
    assert is_placeholder("mzspec:USI000000:run:scan:1")
    assert not is_placeholder("mzspec:PXD000001:run:scan:1")


@pytest.mark.parametrize("acc", ["PXD000561", "RPXD006668", "PXL000001", "MSV000079514", "RMSV000078556"])
def test_collection_pattern_accepts(acc):
    assert re.match(COLLECTION_PATTERN, acc)


@pytest.mark.parametrize("acc", ["USI000000", "10.1234/abc", "PXD1234", "MSV00007951", "pxd000561"])
def test_collection_pattern_rejects(acc):
    assert not re.match(COLLECTION_PATTERN, acc)
