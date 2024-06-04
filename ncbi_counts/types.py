#!/usr/bin/env python

from pathlib import Path
from typing import Literal, Union


StrPath = Union[str, Path]
GseAcc = str
GsmAcc = str
Groups = Union[Literal["treatment", "control"], str]
PairRegex = dict[Groups, dict[str, str]]
GeoRegex = dict[GseAcc, list[PairRegex]]
PairGsms = dict[Groups, list[GsmAcc]]
CountNorm = Literal["fpkm", "tpm"]
AnnotColumn = Literal[
    "Symbol",
    "Description",
    "Synonyms",
    "GeneType",
    "EnsemblGeneID",
    "Status",
    "ChrAcc",
    "ChrStart",
    "ChrStop",
    "Orientation",
    "Length",
    "GOFunctionID",
    "GOProcessID",
    "GOComponentID",
    "GOFunction",
    "GOProcess",
    "GOComponent",
]
AnnotColumns = list[AnnotColumn]
