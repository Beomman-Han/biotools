# biotools

This is a project for providing functions to handle biological data (e.g. ngs data). Currently, the project supports functions for fasta and vcf format data. Our plan is to provide more functions for data of other formats as well as fasta/vcf. For inquiries related to this project, please contact us below.  
@Beomman-Han @mellowo @cyruinous

## Installation
Package could be installed with below command (python >= 3.7).
```sh
tar zxvf biotools.tar.gz
cd biotools
python setup.py install
```

## Quick Start
### FASTA
```python
import FASTA

## init FASTA instance
path = '/path/to/fasta'
fasta = FASTA.FASTA(path)

## open .fa file
fasta.open()

## read by each entry
for seq in fasta.reader():  ## Seq instance
    print(Seq)

## init Seq instance
sequence = 'ACGTAAACGTCCGTGAT'
seq = FASTA.Seq(sequence)

## get reverse/complement sequence
rev_seq = seq.reverse()
com_seq = seq.complement()
rev_com_seq = seq.reverse_complement()

## count base
a_count = seq.count('A')

## calculate gc ratio
gc_content = seq.cal_gc_ratio()

## transcribe DNA seq
dna_sequence = 'ACGTCCCGTAGTCAGTCC'
rna_seq = Seq(dna_sequence).transcribe()

## translate RNA seq
rna_sequence = 'ACUUUGUCAUGUUGCAUGUAU'
protein_seq = Seq(rna_sequence, 'RNA').translate()
```

### VCF
```python
import VCF

## init VCF instance
path = '/path/to/vcf'  ## could be .vcf and .vcf.gz
vcf = VCF.VCF(path)

## sanity check
vcf.sanity_check()  ## True or False

## get meta information
meta_info = vcf.parse_meta_info()  ## dictionary of meta lines

## open .vcf file
vcf.open()

## read by each variant
for var in vcf.reader():  ## varRecord instance
    print(var)

## read by each line
line = vcf.readline()  ## each line (str)

## filter with GT
for line in vcf.get_genotype(['1/1']):  ## alt homo
    print(line)
```