# README

# Authors

Fern Johnson & Samuel Rowlston

# Built with

Python 3

# Modules used

xml.etree.ElementTree
argparse

# Purpose

LRG_Parser is a python script which creates .bed files (a tab delimited text file that stores a genomic data track for bioinformatic analysis) from an LRG XML file.

LRG files are sequences of genes designed specifically for clinical reporting. They are manually curated by experts, information can be fond here https://www.lrg-sequence.org/. 

# Procedure

The script uses an input LRG file in XML format along with two optional parameters - Genome build number (GRCh) and transcript number and produces a .bed file containing the genomic start and finish co-ordinates of all the exons in that gene.

The LRG file must be downloaded prior to using the script and must be within the same file location. An example file can be found here for CASP8: http://ftp.ebi.ac.uk/pub/databases/lrgex/LRG_34.xml  

Script is called using the following arguments:

'-l' or '--LRG'
'-b', '--Build'
'-t', '--Transcript'

LRG is a required argument. The genome build defaults to 'GRCh37.p13'. The transcript defaults to 't1' (transcript 1). 


