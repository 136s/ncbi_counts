#!/usr/bin/env python

from pathlib import Path

import pandas as pd
from yaml import safe_load

from .types import GeoRegex, PairRegex, StrPath


def load_yaml(path: StrPath) -> GeoRegex:
    """Load YAML file

    Args:
        path (StrPath): Path to YAML file.

    Returns:
        GeoRegex: Dictionary of regular expressions.
    """
    with open(path) as f:
        # TODO: validate YAML
        return safe_load(f)


def dataframe_to_dict(regex_df: pd.DataFrame) -> GeoRegex:
    """Convert DataFrame to dictionary of regular expressions.

    Args:
        regex_df (pd.DataFrame): DataFrame of regular expressions.

    Returns:
        GeoRegex: Dictionary of regular expressions.
    """
    use_cols = ["gse", "pair", "group", "attrib", "pattern"]
    assert (
        regex_df.columns.tolist() == use_cols
    ), f"DataFrame columns are invalid: {regex_df.columns.tolist()}"
    regex_dict: GeoRegex = {}
    for (gse_acc, _), gse_pair in regex_df.groupby(["gse", "pair"], sort=False):
        assert gse_acc.startswith("GSE"), "gse column must start with 'GSE'."
        regex_dict.setdefault(gse_acc, [])
        pair: PairRegex = {}
        for group, regex_df in gse_pair.groupby("group", sort=False):
            pair[group] = regex_df.set_index("attrib")["pattern"].to_dict()
        regex_dict[gse_acc].append(pair)
    return regex_dict


def load_csv(csv_path: StrPath, **kwargs) -> GeoRegex:
    """Load CSV file

    Args:
        csv_path (StrPath): Path to CSV file.

    Returns:
        GeoRegex: Dictionary of regular expressions.
    """
    return dataframe_to_dict(pd.read_csv(csv_path, **kwargs))


def load_input(input_path: StrPath) -> GeoRegex:
    """Load input file

    Args:
        input_path (StrPath): Path to input file.

    Raises:
        ValueError: If input file type is not supported.

    Returns:
        GeoRegex: Dictionary of regular expressions.
    """
    match Path(input_path).suffix:
        case ".yaml" | ".yml":
            return load_yaml(input_path)
        case ".csv":
            return load_csv(input_path)
        case ".tsv":
            return load_csv(input_path, sep="\t")
        case _:
            raise ValueError("Supported file types are .yaml, .yml, .csv, .tsv.")
