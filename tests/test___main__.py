#!/usr/bin/env python

import filecmp
from pathlib import Path
import pytest

from ncbi_counts import __main__, utils
from ncbi_counts.types import AnnotColumns, GeoRegex, StrPath

SAMPLE_GEO_REGEX_PATH = Path("tests/data/sample_geo_regex.yaml")
SAMPLE_GEO_REGEX: GeoRegex = {
    "GSE164073": [
        {
            "control": {"title": "Cornea", "characteristics_ch1": "mock"},
            "treatment": {"title": "Cornea", "characteristics_ch1": "SARS-CoV-2"},
        },
        {
            "control": {"title": "Limbus", "characteristics_ch1": "mock"},
            "treatment": {"title": "Limbus", "characteristics_ch1": "SARS-CoV-2"},
        },
        {
            "control": {"geo_accession": "^GSM499609[6-8]$"},
            "treatment": {"geo_accession": "^GSM4996099$|^GSM4996100$|^GSM4996101$"},
        },
    ],
    "GSE63966": [
        {"control": {"title": "LP-C"}, "treatment": {"title": "LP-A"}},
        {"control": {"title": "HM3-C"}, "treatment": {"title": "HM3-A"}},
        {"control": {"title": "HPM3-C"}, "treatment": {"title": "HPM3-A"}},
        {"control": {"title": "HPM4-C"}, "treatment": {"title": "HPM4-A"}},
    ],
}


@pytest.fixture
def sample_input() -> Path:
    utils.save_yaml(SAMPLE_GEO_REGEX, SAMPLE_GEO_REGEX_PATH)
    return SAMPLE_GEO_REGEX_PATH


def test_main(sample_input: Path) -> None:
    geo_regex_path = sample_input
    count_norm_type: str | None = None
    count_annot_ver: str = "GRCh38.p13"
    keep_annot: AnnotColumns = ["Symbol", "Description"]
    silent: bool = False
    src_dir: StrPath = "tests/data/raw"
    save_to: StrPath | None = "tests/data/count"
    str_sep: str = "-"
    to_yaml: StrPath | None = "tests/data/sample_gsms.yaml"
    cleanup: bool = True

    __main__.main(
        geo_regex_path=geo_regex_path,
        count_norm_type=count_norm_type,
        count_annot_ver=count_annot_ver,
        keep_annot=keep_annot,
        src_dir=src_dir,
        save_to=save_to,
        silent=silent,
        str_sep=str_sep,
        to_yaml=to_yaml,
        cleanup=cleanup,
    )

    # python -m ncbi_counts -a GRCh38.p13 -k Symbol Description -s tests/data/expected/raw -o tests/data/expected/count -S - -y tests/data/expected/sample_gsms.yaml -c tests/data/sample_geo_regex.yaml
    expected_dir = Path("tests/data/expected")
    for path in expected_dir.glob("**/*.*"):
        actual_path = expected_dir.parent.joinpath(path.relative_to(expected_dir))
        assert actual_path.is_file(), f"Missing {actual_path}"
        assert filecmp.cmp(path, actual_path, shallow=False), f"Differs {actual_path}"
