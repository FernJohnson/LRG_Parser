import xml.etree.ElementTree as ET
import sys

"""

Parses LRG XML file inout to find exon locations. 

Args = LRG file ... 

"""
# Find LRG file from command line
#script, LRG_file = sys.argv

def parseXML():

    # parses xml, find the room of the structure
    tree = ET.parse('LRG_34.xml') # Using test XML 
    root = tree.getroot()
    
    # Find the chromosome number - this is found under fixed annotation.
    mapping = root.find("./updatable_annotation/annotation_set/mapping")
    chrom = mapping.get('other_name')
    chromosome='chr'+chrom
    
    ## Get LRG ID number for adding to file name
    LRG_ID_num = root.find("./fixed_annotation/id").text
    
    return root, chromosome, LRG_ID_num

def getExons(root):    
    
    
    #find all the exons where the transcript name is 't1'
    exons = root.findall("./fixed_annotation/transcript[@name='t1']/exon") 

    #For each exon, start the start and end values for the first set of coordinates (LRG)
    
    start = []
    end = []
    for exon in exons:
        s = exon[0].get('start')
        e = exon[0].get('end')
        start.append(s)
        end.append(e)
    

    return start, end



def converttoGenome(root, start, end):

    
    #NOTE only picks the first build (37 right now)

    mapping = root.find("./updatable_annotation/annotation_set/mapping")
    
    # Find the other start - this will convert to a genome build coordinates
    otherstart = mapping.get('other_start')
    #We must convert the string to int
    otherstartint = int(otherstart)
    
    #NOTE only picks the first build (37 right now)
    genbuild = mapping.get('coord_system')

    #Tify up the buildname so it can be used in the BedFile name
    genstring=genbuild[0:6]+'_' + genbuild[7:10]


    #Convert lrg exon coordinates using 'other start' into genome coords - for build 37 only now!

    start_gen = [int(x)+otherstartint for x in start]
    end_gen = [int(x)+otherstartint for x in end]
    
    return genstring, start_gen, end_gen

def writeBedFile(LRG_ID_num, genstring, chromosome, start_gen, end_gen):

    # Creating bed file 


    bedfile = open(f'{LRG_ID_num}_{genstring}.bed', "w")
    
    bedfile.write("Chrom" + "\t" + "Start" + "\t" + "End" + "\n")
    for i in range(len(start_gen)):
        bedfile.write(chromosome + "\t" + str(start_gen[i]) + "\t" + str(end_gen[i]) + "\n")

    bedfile.close()

def main():
    root, chromosome, LRG_ID_num = parseXML()
    start, end = getExons(root)
    genstring, start_gen, end_gen = converttoGenome(root, start, end)
    writeBedFile(LRG_ID_num,genstring, chromosome, start_gen, end_gen)

if __name__ == "__main__":
    main()