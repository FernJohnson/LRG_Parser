import xml.etree.ElementTree as ET
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-l', '--LRG', required=True, dest="LRG_File", help='The LRG xml file to be processed')
parser.add_argument('-b', '--Build', default='GRCh37.p13', dest="BuildName", help='Human genome build to use')
parser.add_argument('-t', '--Transcript', default='t1', dest="Transcript", help='Which LRG transcript to use')

results = parser.parse_args()

BuildName = results.BuildName
LRG_file = results.LRG_File
Transcript = results.Transcript


#BuildName = "GRCh38.p12"
#LRG_file = 'LRG_34.xml'
#Transcript = "t1"

#Script, LRG_file, BuildName, Transcript = sys.argv

"""

Parses LRG XML file inout to find exon locations. 

Args = LRG_file Build Transcript
    
    Example = FileLocation/LRG_10.xml GRCh37.p13 t1

"""
# Find LRG file from command line
#script, LRG_file = sys.argv

def main():
    root, chromosome, LRG_ID_num = parseXML(LRG_file)
    start, end = getExons(root, Transcript)
    genstring, start_gen, end_gen = converttoGenome(root, start, end, BuildName)
    writeBedFile(LRG_ID_num,genstring, chromosome, start_gen, end_gen)



def parseXML(LRG_file):

    # parses xml, find the room of the structure
    try:
        tree = ET.parse(LRG_file) # Using test XML 
        
    except FileNotFoundError:
            print("File not found, please check name")
    except ParseError:
            print("LRG file not XML format! Please check file")

        
    root = tree.getroot()
    
    # Find the chromosome number - this is found under fixed annotation.
    mapping = root.find("./updatable_annotation/annotation_set/mapping")
    chrom = mapping.get('other_name')
    chromosome='chr'+chrom
    
    ## Get LRG ID number for adding to file name
    LRG_ID_num = root.find("./fixed_annotation/id").text
    
    return root, chromosome, LRG_ID_num

def getExons(root, Transcript):    
    
    
    #find all the exons where the transcript name is 't1'
    exons = root.findall(f"./fixed_annotation/transcript[@name='{Transcript}']/exon") 
     
    #For each exon, start the start and end values for the first set of coordinates (LRG)
    assert ET.iselement(exons[0]), 'Transcript not found in LRG file!'
    
    start = []
    end = []
    
    for exon in exons:
        s = exon[0].get('start')
        e = exon[0].get('end')
        start.append(s)
        end.append(e)
    

    return start, end


def converttoGenome(root, start, end, BuildName):

    # uses build name from comman line. ****Currently hard coded to be GRCh37.p13****
    
    
    GenomicReference = root.find(f"./updatable_annotation/annotation_set/mapping[@coord_system='{BuildName}']/")
    # Find the other start - this will convert to a genome build coordinates
    
    assert ET.iselement(GenomicReference), 'Genome Build not found, please check build'
    
    Strand = int(GenomicReference.get('strand'))
    if Strand == -1:
        otherstart = GenomicReference.get('other_end')
        
        #We must convert the string to int
        otherstartint = int(otherstart)
    
        #Convert lrg exon coordinates using 'other start' into genome coords
        start_gen = [int(x)-(otherstartint+1) for x in start]
        end_gen = [int(x)-(otherstartint+1) for x in end]
        
        
    else:
        otherstart = GenomicReference.get('other_start')
    
        #We must convert the string to int
        otherstartint = int(otherstart)
    
        #Convert lrg exon coordinates using 'other start' into genome coords
        start_gen = [int(x)+(otherstartint-1) for x in start]
        end_gen = [int(x)+(otherstartint-1) for x in end]
        
       
    #Tidy up the buildname so it can be used in the BedFile name
    genstring=BuildName[0:6] +'-' + BuildName[7:10]


    return genstring, start_gen, end_gen

def writeBedFile(LRG_ID_num, genstring, chromosome, start_gen, end_gen):

    # Creating bed file 


    bedfile = open(f'{LRG_ID_num}_{genstring}_{Transcript}.bed', "w")
    
    bedfile.write("Chrom" + "\t" + "Start" + "\t" + "End" + "\n")
    for i in range(len(start_gen)):
        bedfile.write(chromosome + "\t" + str(start_gen[i]) + "\t" + str(end_gen[i]) + "\n")

    bedfile.close()

if __name__ == "__main__":
    main()
