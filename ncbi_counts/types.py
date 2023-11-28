#!/usr/bin/env python

from pathlib import Path
from typing import Literal


StrPath = str | Path
GseAcc = str
GsmAcc = str
Groups = Literal["treatment", "control"] | str
PairRegex = dict[Groups, dict[str, str]]
GeoRegex = dict[GseAcc, list[PairRegex]]
PairGsms = dict[Groups, list[GsmAcc]]
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
