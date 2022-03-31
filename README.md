# mg-bio

Project for supporting various functions relating bioinformatics. Currently, the project supports functions for FASTA and VCF format files. We have plan to provide functions for files in other formats as well as FASTA/VCF. For inquiries related to this project, please contact us below.

@Beomman-Han
@mellowo
@cyruinous

<br/>

## Pre-requisite
Codes in mg-bio are tested with Python >= 3.9.6 and contains below python modules.

- re, json, gzip

If your python does not have modules, please install modules with pip command or else.

```sh
$ pip install re, json, gzip
```

<br/>

## Install
Please download codes from git repository.
```sh
$ git clone https://github.com/Beomman-Han/mg-bio.git
```

And please add path of directory containing mg-bio project below python statement.

```python
import sys
sys.path.append(mg_bio_path)
```

<br/>

## Example

### FASTA

```python
from mgbio import FASTA

## Init FASTA instance
path = '/path/to/fasta'
fasta = FASTA.FASTA(path)

## Open .fa file
fasta.open()

## Read by line
for line in fasta.reader():
    print(line)
```

<br/>

### VCF

```python
from mgbio import VCF

## Init VCF instance
path = '/path/to/vcf'
vcf = VCF.VCF(path)

## Open .vcf file
vcf.open()

## Read one line
print(vcf.readline())
```

<br/>

## Style Guide

### Naming Convention

1) ClassName : PascalCase

2) function_name (or method_name) : snake_case

3) variable_name : snake_case

4) CONSTANT_NAME : SNAKE_CASE_WITH_UPPER_CASE

5) Recommend using plural format (ex. sequences <- list of sequence)

```python
class SeqRecord:
    ...

def export_to_json(self,
    output_name : str,
    seq_dict : dict = False
    ) -> None:

BASE_IUPAC = {
    'A', 'C', 'G', 'T',
    'U', 'R', 'Y', 'M',
    'K', 'W', 'S', 'B',
    'D', 'H', 'V', 'N'
}
```

<br/>

### Commit Guide

1) Commit every modification of the project

2) Please write commit message in detail

3) Codes must be flawless when the codes are committed
