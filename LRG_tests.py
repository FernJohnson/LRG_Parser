from workingcode import parseXML, getExons, converttoGenome, writeBedFile

import xml.etree.ElementTree as ET
import sys


tree = ET.parse('LRG_12.xml')
root = tree.getroot()



#If the number of exon start and end coordinates aren't equal, something has gone wrong.

start, end = getExons(root, 't1')
assert len(start) == len(end), "Number of start and end coordinates do not match"

start_gen = []
end_gen =[]

genstring, start_gen, end_gen = converttoGenome(root, start, end, 'GRCh37.p13')

#If the number of coordinates don't match after conversion, something has also gone wrong


assert len(start_gen) == len(end_gen), "Number of converted start and end coordinates do not match"



#The start of the first exon in LRG12 should be 99352 - if it's not, either the file or something in the parser has changed.
#If this has changed when it should, it needs to be investigated.

assert start_gen[0] == 99352, "Warning, coordinate values have changed from expected!"
