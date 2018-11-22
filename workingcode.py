import xml.etree.ElementTree as ET

"""

Parses LRG XML file to fin exon locations. 


"""

#parse xml, find the room of the structure
tree = ET.parse('LRG_34.xml') # Using test XML
root = tree.getroot()

#print the tag and attribute of each child in the root

for child in root:
    print(child.tag, child.attrib)
    
#find all annotations in the transcript
transcripts  = root.findall("./fixed_annotation/transcript") #Reference to list of exons in this file

print(len(transcripts))
print(transcripts)


#find all the exons where the transcript name is 't1'
v = root.findall("./fixed_annotation/transcript[@name='t1']/exon") 
# len(v) = 41 = number of exons

#for each exon print the first attribute (the LRG_exon)
#for exon in v:
 #   #print(exon.attrib)
  #  print(exon[0].attrib)
    
start = []
end = []

#for exon in v:
 #   for a in exon[0].items():
        #start += a
        #rint(a)

# print(start)

# for each exon, start the start and end values for the first set of coordinates (LRG)

for exon in v:
    s = exon[0].get('start')
    e = exon[0].get('end')
    start.append(s)
    end.append(e)
    
# print(start, "\n", end)


# Find the chromosome number - this is found under fixed annotation.

n = root.find("./updatable_annotation/annotation_set/mapping")
chrom = n.get('other_name')

# Creating bed file with headers

bedfile = open("Bedfile.txt", "w")

bedfile.write("Chrom" + "\t" + "Start" + "\t" + "End" + "\n")
for i in range(len(start)):
    bedfile.write(chrom + "\t" + start[i] + "\t" + end[i] + "\n")

bedfile.close()
