#!/usr/bin/env python

from pathlib import Path
from setuptools import setup, find_packages

NAME = "ncbi_counts"
HERE = Path(__file__).resolve().parent

about = {}
with open(HERE.joinpath(NAME, "__version__.py")) as f:
    exec(f.read(), about)

setup(
    name=NAME,
    version=about.get("__version__"),
    description="Download the NCBI-generated RNA-seq count data by specifying the Series accession number(s), and the regular expression of the Sample attributes.",
    author="Yuki SUYAMA",
    url="https://github.com/136s/ncbi_counts",
    packages=find_packages(exclude=("tests", "docs")),
    python_requires=">=3.10.0",
    install_requires=["GEOparse", "pandas", "PyYAML"],
    keywords=["GEO", "Gene Expression Omnibus", "Bioinformatics", "RNA-seq", "NCBI"],
)
