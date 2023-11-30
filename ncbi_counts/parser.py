#!/usr/bin/env python

import argparse
from pathlib import Path

from ncbi_counts.types import AnnotColumn, CountNorm


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="ncbi_counts",
        description="Download the NCBI-generated RNA-seq count data by specifying the Series accession number(s), and the regular expression of the Sample attributes.",
    )
    parser.add_argument(
        "input",
        metavar="FILE",
        type=Path,
        help="""
        Path to input file (.yaml, .yml) which represents each GSE accession number(s)
        which contains a sequence of maps with two keys: 'control' and 'treatment'.
        Each of these maps further contains key(s) (e.g., 'title', 'characteristics_ch1').
        """,
    )
    parser.add_argument(
        "-n",
        "--norm-type",
        metavar="NORM",
        type=CountNorm,
        choices=[None] + [a for a in CountNorm.__args__],
        default=None,
        help=f'Normalization type of counts (choices: None, {", ".join(CountNorm.__args__)}, default: None)',
    )
    parser.add_argument(
        "-a",
        "--annot-ver",
        metavar="ANNOT_VER",
        type=str,
        default="GRCh38.p13",
        help="Annotation version of counts (default: GRCh38.p13)",
    )
    parser.add_argument(
        "-k",
        "--keep-annot",
        metavar="KEEP_ANNOT",
        nargs="*",
        type=str,
        choices=AnnotColumn.__args__,
        default=[],
        help=f'Annotation column(s) to keep (choices: {", ".join(AnnotColumn.__args__)}, default: None)',
    )
    parser.add_argument(
        "-s",
        "--src-dir",
        type=Path,
        default=Path(),
        help="A directory to save the source obtained from NCBI (default: ./)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(),
        help="A directory to save the count matrix (or matrices) (default: ./)",
    )
    parser.add_argument(
        "-q",
        "--silent",
        default=False,
        action="store_true",
        help="If True, suppress warnings (default: False)",
    )
    parser.add_argument(
        "-S",
        "--sep",
        type=str,
        default="-",
        help="Separator between group and GSM in column (default: -)",
    )
    parser.add_argument(
        "-y",
        "--yaml",
        metavar="GSM_YAML",
        type=Path,
        default=None,
        help="Path to save YAML file which contains GSMs (default: None)",
    )
    return parser.parse_args()
