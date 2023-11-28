# ncbi_counts

Download the [NCBI-generated RNA-seq count data](https://www.ncbi.nlm.nih.gov/geo/info/rnaseqcounts.html) by specifying the Series accession number(s), and the regular expression of the Sample attributes.

If you just need a count for all samples (GSM) in a series (GSE), this library is not needed. However, if you need a count matrix for each GSE, specifying only the control group samples and treatment group samples, this library may be useful.

## Usage

To create a mock vs. CoV2 comparison pair for each tissues from [GSE164073](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE164073), please prepare the following yaml file (but do not need words beginning with "!!" as they are type hints):

```sample_regex.yaml
GSE164073: !!seq
- treatment: !!map
    title: !!str Cornea
    characteristics_ch1: !!str SARS-CoV-2
  control: !!map
    title: !!str Cornea
    characteristics_ch1: !!str mock
- treatment: !!map
    title: !!str Limbus
    characteristics_ch1: !!str SARS-CoV-2
  control: !!map
    title: !!str Limbus
    characteristics_ch1: !!str mock
- treatment: !!map
    title: !!str Sclera
    characteristics_ch1: !!str SARS-CoV-2
  control: !!map
    title: !!str Sclera
    characteristics_ch1: !!str mock
```

and run the following command:

```bash
python -m ncbi_counts sample_regex.yaml --output_dir counts
```
