#!/usr/bin/env python

from pathlib import Path
import re
from typing import Iterable, Literal
import warnings

from GEOparse.downloader import Downloader
from GEOparse.GEOTypes import GSM, HTTPError
import pandas as pd
from yaml import safe_dump

from .types import GseAcc, GsmAcc, PairGsms, PairRegex

GEO_BASE_URL = "https://www.ncbi.nlm.nih.gov"
GEO_DOWNLOAD_BASE = GEO_BASE_URL + "/geo/download/?"


def is_matched(
    attrib_regex: dict[str, str], gsm_metadata: dict, silent: bool = False
) -> bool:
    """Check if GSM metadata matches regex.

    Args:
        attrib_regex (dict[str, str]): a dictionary of regex (value) for each attribute (key)
        gsm_metadata (dict): gsm metadata.
        silent (bool, optional): if True, suppress warnings. Defaults to False.

    Returns:
        bool: if GSM metadata matches regex, return True.
    """
    bools: list[bool] = []
    for attrib, pattern in attrib_regex.items():
        if gsm_metadata.get(attrib) is not None:
            # Check if any of the values match the regex
            metadata_bools = [
                bool(re.search(pattern, v)) for v in gsm_metadata.get(attrib) if v != ""
            ]
            bools.append(any(metadata_bools))
        else:
            if not silent:
                warnings.warn(
                    f"Attribute '{attrib}' not found in {gsm_metadata.get('geo_accession')[0]}"
                )
            bools.append(False)
    # If all attributes match regex, return True
    return all(bools)


def match_pair_gsms(
    pair_regex: PairRegex, gsms: Iterable[GSM], silent: bool = False
) -> PairGsms:
    """Match GSMs to regex.

    Args:
        pair_regex (PairRegex): a dictionary of regex dictionary (value) for each group (key).
        gsms (Iterable[GSM]): GSMs to match.
        silent (bool, optional): if True, suppress warnings. Defaults to False.

    Returns:
        PairGsms: a dictionary of GSMs (value) for each group (key).
    """
    pair_gsms: PairGsms = {}
    for group, group_regex_dict in pair_regex.items():
        matched_gsms: list[GsmAcc] = []
        for gsm_info in gsms:
            if is_matched(group_regex_dict, gsm_info.metadata, silent=silent):
                matched_gsms.append(gsm_info.name)
        if len(matched_gsms):
            pair_gsms[group] = matched_gsms
        else:
            if not silent:
                warnings.warn(f"No GSMs matched for {group}")
    return pair_gsms


def get_count_url(
    gse_acc: GseAcc,
    norm_type: Literal["fpkm", "tpm"] | None = None,
    annot_ver: str = "GRCh38.p13",
) -> str:
    """Get URL of NCBI-generated count file.

    Args:
        gse_acc (GseAcc): GSE accession number.
        norm_type (Literal["fpkm", "tpm"], optional): Normalization type. Defaults to None.
        annot_ver (str, optional): Annotation version. Defaults to "GRCh38.p13".

    Returns:
        str: URL of NCBI-generated count file.
    """
    match norm_type:
        case None:
            count_type = "raw_counts"
        case "fpkm" | "tpm":
            count_type = "norm_counts_" + norm_type.upper()
        case _:
            raise ValueError("Supported normalization types are 'fpkm' and 'tpm'.")
    return (
        GEO_DOWNLOAD_BASE
        + f"type=rnaseq_counts&acc={gse_acc}&format=file&file={gse_acc}_{count_type}_{annot_ver}_NCBI.tsv.gz"
    )


def get_annot_url(spieces: str = "Human", annot_ver: str = "GRCh38.p13") -> str:
    """Get URL of Human gene annotation table file.

    Args:
        spieces (str, optional): Species. Defaults to "Human".
        annot_ver (str, optional): Annotation version. Defaults to "GRCh38.p13".

    Returns:
        str: URL of Human gene annotation table file.
    """
    return (
        GEO_DOWNLOAD_BASE
        + f"format=file&type=rnaseq_counts&file={spieces}.{annot_ver}.annot.tsv.gz"
    )


def parse_filename_from_url(url: str, filename_key: str = "file") -> str:
    """Parse filename from URL.

    Args:
        url (str): URL.
        filename_key (str, optional): Key of filename in URL. Defaults to "file".

    Raises:
        ValueError: If cannot parse filename from URL.

    Returns:
        str: Filename.
    """
    for param in url.split("?")[-1].split("&"):
        key, value = param.split("=")
        if key == filename_key:
            return value
    raise ValueError(f"Cannot parse filename from: {url}")


def download(
    count_url: str, count_path: Path = Path(), force: bool = False, silent: bool = False
) -> Path:
    """Save count file from URL.

    Args:
        count_url (str): URL of count file.
        count_path (Path, optional): file path to save. Defaults to Path().
        force (bool, optional): Defaults to False.
        silent (bool, optional): If True, suppress messages. Defaults to False.

    Raises:
        ValueError: If count_path is a directory.

    Returns:
        Path: file path of count file.
    """
    if count_path.is_dir():
        raise ValueError(f"count_path must be a file path: {count_path}")
    try:
        Downloader(
            count_url, outdir=count_path.parent, filename=count_path.name
        ).download(force=force, silent=silent)
        return count_path
    except HTTPError:
        warnings.warn(f"Cannot download: {count_url}")


def get_count_dataframe(
    count_url: str, count_path: Path = Path(), force: bool = False, silent=False
) -> pd.DataFrame | None:
    """Get count DataFrame from URL.

    Args:
        count_url (str): URL of count file.
        count_path (Path, optional): file path to save. Defaults to Path().
        force (bool, optional): Defaults to False.
        silent (bool, optional): If True, suppress messages. Defaults to False.

    Returns:
        pd.DataFrame | None: Count DataFrame.
    """
    count_path = download(count_url, count_path, force=force, silent=silent)
    if count_path is not None:
        return pd.read_table(count_path, index_col=0, dtype=str)


def construct_pair_count(
    pair_gsms: PairGsms, count: pd.DataFrame, annot: pd.DataFrame | None = None, sep="-"
) -> pd.DataFrame:
    """Construct count DataFrame for paired GSMs.

    Args:
        pair_gsms (PairGsms): a dictionary of GSMs (value) for each group (key).
        count (pd.DataFrame): count DataFrame.
        annot (pd.DataFrame | None, optional): annotation DataFrame. Defaults to None.
        sep (str, optional): separator between group and GSM in column. Defaults to "-".

    Returns:
        pd.DataFrame: count DataFrame for paired GSMs.
    """
    group_df_list: list[pd.DataFrame] = []
    if annot is not None:
        group_df_list.append(annot)
    for group, gsms in pair_gsms.items():
        gsms_in_count = set(count.columns) & set(gsms)
        if len(gsms_in_count) == 0:
            warnings.warn(f"No GSMs matched for {group}")
        else:
            if len(gsms_in_count) < len(gsms):
                warnings.warn(
                    f"Only {len(gsms_in_count)} GSMs matched for {group} out of {len(gsms)}"
                    f" (dropped: {sorted(list(set(gsms) - gsms_in_count))}))"
                )
            group_df_list.append(count[list(gsms_in_count)].add_prefix(group + sep))
    return (
        pd.concat(group_df_list, axis=1)
        .sort_index()
        .set_index(annot.columns.tolist(), append=True)
    )


def save_yaml(d: dict, yaml_path: Path):
    yaml_path.parent.mkdir(parents=True, exist_ok=True)
    with open(yaml_path, "w") as f:
        safe_dump(d, f)
