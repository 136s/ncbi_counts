#!/usr/bin/env python

from dataclasses import dataclass, field
from pathlib import Path
import warnings

from GEOparse import get_GEO
from GEOparse.GEOTypes import GSE
import pandas as pd

from .types import AnnotColumns, GseAcc, PairGsms, PairRegex, StrPath
from .utils import (
    construct_pair_count,
    get_annot_url,
    get_count_dataframe,
    get_count_url,
    match_pair_gsms,
    parse_filename_from_url,
)


@dataclass
class Series:
    gse_acc: GseAcc
    gse_info: GSE = field(init=False, repr=False)
    pair_regex_list: list[PairRegex]
    pair_gsms_list: list[PairGsms] = field(default_factory=list, init=False)
    count_norm_type: str | None = field(default=None)
    count_annot_ver: str = field(default="GRCh38.p13")
    keep_annot: AnnotColumns = field(default_factory=[])
    count_url: str = field(init=False)
    count_path: Path = field(init=False)
    count: pd.DataFrame = field(init=False, repr=False)
    annot_url: str = field(init=False)
    annot_path: Path = field(init=False)
    annot: pd.DataFrame | None = field(default=None, repr=False)
    pair_count_list: list[pd.DataFrame] = field(
        default_factory=list, init=False, repr=False
    )
    pair_count_path_list: list[Path] = field(default_factory=list, init=False)
    src_dir: StrPath = field(default="./")
    save_to: StrPath | None = field(default="./")
    silent: bool = field(default=True)
    str_sep: str = field(default="-")

    def __post_init__(self):
        if not self.gse_acc.startswith("GSE"):
            raise ValueError("GSE accession must start with GSE")
        self.prepare_dirs()
        self.set_gse_info()
        self.match_pair_samples()
        self.set_count_url()
        self.set_count_path()
        if self.keep_annot:
            self.set_annot_url()
            self.set_annot_path()

    def generate_pair_matrix(self):
        self.set_count()
        self.set_annot()
        self.set_pair_count()
        self.set_pair_count_path()
        if self.save_to is not None:
            self.save_pair_count()

    def prepare_dirs(self):
        self.src_dir = Path(self.src_dir)
        self.src_dir.mkdir(parents=True, exist_ok=True)
        if self.save_to is not None:
            self.save_to = Path(self.save_to)
            self.save_to.mkdir(parents=True, exist_ok=True)

    def set_gse_info(self):
        self.gse_info = get_GEO(self.gse_acc, destdir=self.src_dir, silent=self.silent)

    def match_pair_samples(self):
        gsms = self.gse_info.gsms.values()
        matched_regex: list[PairRegex] = []
        for pair_regex in self.pair_regex_list:
            pair_gsms = match_pair_gsms(pair_regex, gsms, silent=self.silent)
            if pair_gsms:
                self.pair_gsms_list.append(pair_gsms)
                matched_regex.append(pair_regex)
            else:
                if not self.silent:
                    warnings.warn(
                        f"Could not find pair samples for {pair_regex}. Skipping..."
                    )
        self.pair_regex_list = matched_regex

    def set_count_url(self):
        self.count_url = get_count_url(
            self.gse_acc, norm_type=self.count_norm_type, annot_ver=self.count_annot_ver
        )

    def set_count_path(self):
        count_filename = parse_filename_from_url(self.count_url)
        self.count_path = self.src_dir.joinpath(count_filename)

    def set_count(self):
        self.count = get_count_dataframe(
            self.count_url, self.count_path, silent=self.silent
        )
        if self.count is None:
            raise ValueError("Could not load count matrix")

    def set_annot_url(self):
        self.annot_url = get_annot_url(annot_ver=self.count_annot_ver)

    def set_annot_path(self):
        annot_filename = parse_filename_from_url(self.annot_url)
        self.annot_path = self.src_dir.joinpath(annot_filename)

    def set_annot(self):
        if self.keep_annot:
            self.annot = get_count_dataframe(
                self.annot_url, self.annot_path, silent=self.silent
            )[self.keep_annot]

    def set_pair_count(self):
        for pair_gsms in self.pair_gsms_list:
            pair_count = construct_pair_count(
                pair_gsms, self.count, annot=self.annot, sep=self.str_sep
            )
            self.pair_count_list.append(pair_count)

    def set_pair_count_path(self, start_index: int = 1):
        digit = len(self.pair_count_list) // 10 + 1
        for i in range(len(self.pair_count_list)):
            self.pair_count_path_list.append(
                self.save_to.joinpath(
                    f"{self.gse_acc}{self.str_sep}{i + start_index:0{digit}}.tsv"
                )
            )

    def save_pair_count(self):
        for pair_count, pair_count_path in zip(
            self.pair_count_list, self.pair_count_path_list
        ):
            pair_count.to_csv(pair_count_path, sep="\t")
