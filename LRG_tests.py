import workingcode as wc
import xml.etree.ElementTree as ET
import sys


tree = ET.parse('LRG_DUMMY.xml')
root = tree.getroot()

#If the number of exon start and end coordinates aren't equal, something has gone wrong.

start, end = getExons(root)
assert start != end, "Number of start and end coordinates do not match"