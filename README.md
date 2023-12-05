# ncbi_counts

Download the [NCBI-generated RNA-seq count data](https://www.ncbi.nlm.nih.gov/geo/info/rnaseqcounts.html) by specifying the Series accession number(s), and the regular expression of the Sample attributes.

If you just need a count matrix for all samples (GSM) in a series (GSE), this library is not needed. However, if you need a count matrix for each GSE, specifying only the control group samples and treatment group samples, this library may be useful.

## Installation

From [PyPI](https://pypi.org/project/ncbi-counts/):

```sh
pip install ncbi-counts
```

## Usage

```sh
python -m ncbi_counts [-h] [-n NORM] [-a ANNOT_VER] [-k [KEEP_ANNOT ...]] [-s SRC_DIR] [-o OUTPUT] [-q] [-S SEP] [-y GSM_YAML] [-c] FILE
```

### Options

```sh
positional arguments:
  FILE                  Path to input file (.yaml, .yml) which represents each GSE accession number(s) which contains a sequence of maps with two keys: 'control' and 'treatment'. Each of these maps further contains key(s) (e.g., 'title', 'characteristics_ch1').

options:
  -h, --help            show this help message and exit
  -n NORM, --norm-type NORM
                        Normalization type of counts (choices: None, fpkm, tpm, default: None)
  -a ANNOT_VER, --annot-ver ANNOT_VER
                        Annotation version of counts (default: GRCh38.p13)
  -k [KEEP_ANNOT ...], --keep-annot [KEEP_ANNOT ...]
                        Annotation column(s) to keep (choices: Symbol, Description, Synonyms, GeneType, EnsemblGeneID, Status, ChrAcc, ChrStart, ChrStop, Orientation, Length, GOFunctionID, GOProcessID, GOComponentID, GOFunction, GOProcess, GOComponent, default: None)
  -s SRC_DIR, --src-dir SRC_DIR
                        A directory to save the source obtained from NCBI (default: ./)
  -o OUTPUT, --output OUTPUT
                        A directory to save the count matrix (or matrices) (default: ./)
  -q, --silent          If True, suppress warnings (default: False)
  -S SEP, --sep SEP     Separator between group and GSM in column (default: -)
  -y GSM_YAML, --yaml GSM_YAML
                        Path to save YAML file which contains GSMs (default: None)
  -c, --cleanup         If True, remove source files (default: False)
```

### Command-line Example

To create a mock vs. CoV2 comparison pair for each tissues from [GSE164073](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE164073), please prepare the following yaml file (but do not need words beginning with "!!" as they are type hints):

> [!NOTE]
> The acceptable options for Sample attributes (such as 'title' and 'characteristics_ch1') can be found on the [Sample Attributes](https://www.ncbi.nlm.nih.gov/geo/info/soft.html#sample_tab) table or [SOFT download](https://www.ncbi.nlm.nih.gov/geo/info/soft.html#download) section in [SOFT submission instructions](https://www.ncbi.nlm.nih.gov/geo/info/soft.html) page.
> You can use the values in the 'Label' column of the table as a key in the YAML file. Also, please exclude the string '!Sample_'.
>
> If you want a comprehensive list of attributes for all samples in a series, [`GEOparse` library](https://geoparse.readthedocs.io/en/latest/GEOparse.html#GEOparse.GEOTypes.GSE.phenotype_data) is useful.
>
> ```python
>  import GEOparse
>  GEOparse.get_GEO("GSExxxxx").phenotype_data
> ```

```sample_regex.yaml
GSE164073: !!seq
- control: !!map
    title: !!str Cornea
    characteristics_ch1: !!str mock
  treatment: !!map
    title: !!str Cornea
    characteristics_ch1: !!str SARS-CoV-2
- control: !!map
    title: !!str Limbus
    characteristics_ch1: !!str mock
  treatment: !!map
    title: !!str Limbus
    characteristics_ch1: !!str SARS-CoV-2
- control: !!map
    title: !!str Sclera
    characteristics_ch1: !!str mock
  treatment: !!map
    title: !!str Sclera
    characteristics_ch1: !!str SARS-CoV-2
```

or if you would like to specify the GSM directly, please prepare the following yaml file:

```samples.yaml
GSE164073: !!seq
- control: !!map
    geo_accession: !!str ^GSM4996084$|^GSM4996085$|^GSM4996086$
  treatment: !!map
    geo_accession: !!str ^GSM4996087$|^GSM4996088$|^GSM4996089$
- control: !!map
    geo_accession: !!str ^GSM4996090$|^GSM4996091$|^GSM4996092$
  treatment: !!map
    geo_accession: !!str ^GSM4996093$|^GSM4996094$|^GSM4996095$
- control: !!map
    geo_accession: !!str ^GSM4996096$|^GSM4996097$|^GSM4996098$
  treatment: !!map
    geo_accession: !!str ^GSM4996099$|^GSM4996100$|^GSM4996101$
```

and run the following command ("Symbol" column is kept in this expample):

```sh
python -m ncbi_counts sample_regex.yaml -k Symbol -c
```

then you will get the following files:

<details open><summary>GSE164073-1.tsv</summary>

|GeneID|Symbol|control-GSM4996084|control-GSM4996085|control-GSM4996086|treatment-GSM4996088|treatment-GSM4996087|treatment-GSM4996089|
|:----|:----|:----|:----|:----|:----|:----|:----|
|1|A1BG|144|197|157|156|133|122|
|2|A2M|254|276|262|178|153|178|
|3|A2MP1|1|0|2|0|0|0|
|9|NAT1|97|133|103|83|93|88|
|...|...|...|...|...|...|...|...|
</details>
<details><summary>GSE164073-2.tsv</summary>

|GeneID|Symbol|control-GSM4996092|control-GSM4996091|control-GSM4996090|treatment-GSM4996095|treatment-GSM4996094|treatment-GSM4996093|
|:----|:----|:----|:----|:----|:----|:----|:----|
|1|A1BG|175|167|203|143|145|145|
|2|A2M|261|158|427|215|145|169|
|3|A2MP1|0|0|0|0|0|2|
|9|NAT1|122|100|133|90|78|80|
|...|...|...|...|...|...|...|...|
</details>

<details><summary>GSE164073-3.tsv</summary>

|GeneID|Symbol|control-GSM4996098|control-GSM4996097|control-GSM4996096|treatment-GSM4996099|treatment-GSM4996100|treatment-GSM4996101|
|:----|:----|:----|:----|:----|:----|:----|:----|
|1|A1BG|158|115|140|136|124|145|
|2|A2M|3337|2261|2536|1524|1288|1807|
|3|A2MP1|0|0|0|0|0|0|
|9|NAT1|83|64|68|65|52|79|
|...|...|...|...|...|...|...|...|
</details>

If you don't need source files from NCBI, please delete the following files:

### Example in Python

To get the output as a pandas DataFrame, please refer to the following code:

```python
from ncbi_counts import Series

series = Series(
    "GSE164073",
    [
        {
            "control": {"title": "Cornea", "characteristics_ch1": "mock"},
            "treatment": {"title": "Cornea", "characteristics_ch1": "SARS-CoV-2"},
        },
        {
            "control": {"title": "Limbus", "characteristics_ch1": "mock"},
            "treatment": {"title": "Limbus", "characteristics_ch1": "SARS-CoV-2"},
        },
        {
            "control": {"geo_accession": "^GSM499609[6-8]$"},
            "treatment": {"geo_accession": "^GSM4996099$|^GSM4996100$|^GSM4996101$"},
        },
    ],
    keep_annot=["Symbol"],
    save_to=None,
)
series.generate_pair_matrix()
# series.cleanup()  # remove source files
series.pair_count_list[0]  # Corresponds to GSE164073-1.tsv
series.pair_count_list[1]  # Corresponds to GSE164073-2.tsv
series.pair_count_list[2]  # Corresponds to GSE164073-3.tsv
```

## License

ncbi_counts is released under an [MIT license](LICENSE).
