# README

## Authors

Fern Johnson & Samuel Rowlston

## Built with

Python 3

## Modules used

*  xml.etree.ElementTree
*  argparse

## Purpose

`LRG_Parser.py` is a python script which creates .bed files (a tab delimited text file that stores a genomic data track for bioinformatic analysis) from an LRG XML formatted file.

LRG files are sequences of genes designed specifically for clinical reporting. They are manually curated by experts, further information on LRG sequences can be found [here](https://www.lrg-sequence.org/). 

## Procedure

The script (`LRG_Parser.py`) uses an input LRG file in XML format along with two optional parameters - Genome build number (GRCh) and transcript number and produces a .bed file containing the genomic start and finish co-ordinates of all the exons in that gene.

The LRG file must be downloaded prior to using the script and must be within the same directory as the script. An example file can be found [here](http://ftp.ebi.ac.uk/pub/databases/lrgex/LRG_34.xml) for CASP8   

The script is called using the following arguments:

```

*  '-l' or '--LRG'
*  '-b' or '--Build'
*  '-t' or '--Transcript'

```

LRG is a required argument. The genome build defaults to `GRCh37.p13`. The transcript defaults to `t1` (transcript 1). 

Example use:

```python
python LRG_Parser -l LRG_34.xml -b GRCh37.p13 -t t1
```

## Testing

The `LRG_tests.py` script performs quality checks on the `LRG_Parser.py` to ensure it functions as expected after any modification is made.

The LRG file `LRG_12.xml` is used to test the script, click [here](http://ftp.ebi.ac.uk/pub/databases/lrgex/LRG_12.xml) to find it. Please ensure that you have this LRG file downloaded and in the same directory as the script. 

If the script functions as intended there will be no output when the `LRG_tests.py` script is run. 

