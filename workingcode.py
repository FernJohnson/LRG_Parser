import xml.etree.ElementTree as ET
import sys

"""

Parses LRG XML file inout to find exon locations. 

Args = LRG file ... 

"""
# Find LRG file from command line
#script, LRG_file = sys.argv



# parses xml, find the room of the structure
tree = ET.parse('LRG_34.xml') # Using test XML 
root = tree.getroot()

#print the tag and attribute of each child in the root

for child in root:
    print(child.tag, child.attrib)
    
#find all annotations in the transcript
transcripts  = root.findall("./fixed_annotation/transcript") #Reference to list of exons in this file

# Get LRG ID number for adding to file name
LRG_ID_num = root.find("./fixed_annotation/id").text

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
# Find the other start - this will convert to a genome build coordinates
#NOTE only picks the first build (37 right now)

n = root.find("./updatable_annotation/annotation_set/mapping")
chrom = n.get('other_name')
otherstart = n.get('other_start')
genbuild = n.get('coord_system')


genstring=genbuild[0:6]+'_' + genbuild[7:10]


#print(type(otherstart))
otherstartint = int(otherstart)

chromosome='chr'+chrom
print(chromosome)

#Convert lrg exon coordinates using 'other start' into genome coords - for build 37!

start_gen = [int(x)+otherstartint for x in start]
end_gen = [int(x)+otherstartint for x in end]

print(start_gen)
print(end_gen)

# Creating bed file with headers



bedfile = open(f'{LRG_ID_num}_{genstring}.bed', "w")

bedfile.write("Chrom" + "\t" + "Start" + "\t" + "End" + "\n")
for i in range(len(start)):
    bedfile.write(chromosome + "\t" + str(start_gen[i]) + "\t" + str(end_gen[i]) + "\n")

bedfile.close()
