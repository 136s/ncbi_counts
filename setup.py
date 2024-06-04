#!/usr/bin/env python
from pathlib import Path
from setuptools import setup, find_packages

NAME = "ncbi_counts"
HERE = Path(__file__).resolve().parent


def readme():
    with open(HERE.joinpath("README.md")) as f:
        return f.read()


about = {}
with open(HERE.joinpath(NAME, "__version__.py")) as f:
    exec(f.read(), about)

setup(
    name=NAME,
    version=about.get("__version__"),
    description="Download the NCBI-generated RNA-seq count data by specifying the Series accession number(s), and the regular expression of the Sample attributes.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Yuki SUYAMA",
    license="MIT",
    classifiers=[
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    url="https://github.com/136s/ncbi_counts",
    packages=find_packages(exclude=("tests", "docs")),
    python_requires=">=3.9.0",
    install_requires=["GEOparse", "pandas", "PyYAML"],
    extras_require={"dev": ["pytest", "build", "twine"]},
    keywords=["GEO", "Gene Expression Omnibus", "Bioinformatics", "RNA-seq", "NCBI"],
)
