#!/usr/bin/env python

from pathlib import Path

from .core import Series
from .load import load_input
from .parser import parse_args
from .types import AnnotColumns, CountNorm, GseAcc, PairGsms, StrPath
from .utils import save_yaml


def main(
    geo_regex_path: StrPath,
    count_norm_type: CountNorm | None = None,
    count_annot_ver: str = "GRCh38.p13",
    keep_annot: AnnotColumns = [],
    src_dir: StrPath = "./",
    save_to: StrPath | None = "./",
    silent: bool = False,
    str_sep: str = "-",
    to_yaml: StrPath = None,
) -> dict[GseAcc, Series]:
    """Generate count matrix for each series.

    Args:
        geo_regex_path (StrPath): path to input file (.yaml, .yml, .csv, .tsv).
        count_norm_type (CountNorm | None, optional): normalization type. Defaults to None.
        count_annot_ver (str, optional): annotation version. Defaults to "GRCh38.p13".
        keep_annot (AnnotColumns, optional): annotation columns to keep. Defaults to [].
        src_dir (StrPath, optional): source directory. Defaults to "./".
        save_to (StrPath | None, optional): save directory. Defaults to "./".
        silent (bool, optional): if True, suppress warnings. Defaults to False.
        str_sep (str, optional): separator between group and GSM in column. Defaults to "-".
        to_yaml (StrPath, optional): path to save YAML file. Defaults to None.

    Returns:
        dict[GseAcc, Series]: a dictionary of Series (value) for each series (key).
    """
    regex_dict = load_input(geo_regex_path)
    series_dict: dict[GseAcc, Series] = {}
    if to_yaml is not None:
        samples_dict: dict[GseAcc, list[PairGsms]] = {}
    for gse, pair_regex_list in regex_dict.items():
        series = Series(
            gse_acc=gse,
            pair_regex_list=pair_regex_list.copy(),
            count_norm_type=count_norm_type,
            count_annot_ver=count_annot_ver,
            keep_annot=keep_annot,
            src_dir=src_dir,
            save_to=save_to,
            silent=silent,
            str_sep=str_sep,
        )
        series.generate_pair_matrix()
        series_dict[gse] = series
        if to_yaml is not None:
            samples_dict[gse] = series.pair_gsms_list
    if to_yaml is not None:
        save_yaml(samples_dict, Path(to_yaml))
    return series_dict


if __name__ == "__main__":
    args = parse_args()

    geo_regex_path: StrPath = args.input
    count_norm_type: str | None = args.norm_type
    count_annot_ver: str = args.annot_ver
    keep_annot: AnnotColumns = args.keep_annot
    src_dir: StrPath = args.src_dir
    save_to: StrPath | None = args.output
    silent: bool = args.silent
    str_sep: str = args.sep
    to_yaml: StrPath = args.yaml

    series_dict = main(
        geo_regex_path=geo_regex_path,
        count_norm_type=count_norm_type,
        count_annot_ver=count_annot_ver,
        keep_annot=keep_annot,
        src_dir=src_dir,
        save_to=save_to,
        silent=silent,
        str_sep=str_sep,
        to_yaml=to_yaml,
    )
