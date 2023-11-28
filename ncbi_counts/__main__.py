#!/usr/bin/env python

from pathlib import Path
from ncbi_counts.core import Series
from ncbi_counts.types import AnnotColumns, GeoRegex, GseAcc, PairGsms, StrPath
from ncbi_counts.utils import save_yaml


def main(
    regex_dict: GeoRegex,
    count_norm_type: str | None = None,
    count_annot_ver: str = "GRCh38.p13",
    keep_annot: AnnotColumns = [],
    src_dir: StrPath = "./",
    save_to: StrPath | None = "./",
    silent: bool = True,
    str_sep: str = "-",
    to_yaml: StrPath = None,
) -> dict[GseAcc, Series]:
    series_dict: dict[GseAcc, Series] = {}
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
    count_norm_type: str | None = None
    count_annot_ver: str = "GRCh38.p13"
    keep_annot: AnnotColumns = []
    src_dir: StrPath = "./"
    save_to: StrPath | None = "./"
    silent: bool = True
    str_sep: str = "-"
    to_yaml: StrPath = None
