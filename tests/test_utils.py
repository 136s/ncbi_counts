#!/usr/bin/env python

import pytest

from ncbi_counts import utils

params_is_matched = [
    ({"title": "Cornea", "characteristics_ch1": "mock"}, True),
    ({"title": "Cornea", "characteristics_ch1": "SARS-CoV-2"}, False),
]


@pytest.mark.parametrize("attrib_regex, expected", params_is_matched)
def test_is_matched(attrib_regex, expected):
    gsm_metadata = {
        "title": ["Cornea_mock_1"],
        "geo_accession": ["GSM4996084"],
        "characteristics_ch1": [
            "tissue: cornea",
            "infection: mock",
            "time point: 24 hours",
        ],
    }
    assert utils.is_matched(attrib_regex, gsm_metadata) is expected
