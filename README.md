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

LRG files are sequences of genes designed specifically for clinical reporting. They are manually curated by experts (https://www.lrg-sequence.org/), .

The script uses an input LRG file in XML format along with two optional parameters - Genome build number (GRCh) and transcript number and produces a .bed file containing the genomic start and finish co-ordinates of all the exons in that gene.


