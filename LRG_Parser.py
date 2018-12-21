import xml.etree.ElementTree as ET
import sys
import argparse


"""

Parses LRG XML file input to find exon locations. 

The script is called using the following arguments:

*  '-l' or '--LRG'
*  '-b' or '--Build'
*  '-t' or '--Transcript'

LRG is a required argument. The genome build defaults to `GRCh37.p13`. The transcript defaults to `t1` (transcript 1). 

Example use:

python LRG_Parser -l LRG_34.xml -b GRCh37.p13 -t t1


"""

def main():
    
    parser = argparse.ArgumentParser()

    # Setting arguments for parser - LRG file, Genome build, Transcript required

    parser.add_argument('-l', '--LRG', required=True, dest="LRG_File", help='The LRG xml file to be processed')
    parser.add_argument('-b', '--Build', default='GRCh37.p13', dest="BuildName", help='Human genome build to use')
    parser.add_argument('-t', '--Transcript', default='t1', dest="Transcript", help='Which LRG transcript to use')

    results = parser.parse_args()

    # Storing inputs in variables

    BuildName = results.BuildName
    LRG_file = results.LRG_File
    Transcript = results.Transcript
    
    root, chromosome, LRG_ID_num = parseXML(LRG_file)
    start, end = getExons(root, Transcript)
    genstring, start_gen, end_gen = converttoGenome(root, start, end, BuildName)
    writeBedFile(LRG_ID_num,genstring, chromosome, start_gen, end_gen, Transcript)

    return BuildName, LRG_file, Transcript

def parseXML(LRG_file):

    # Parses xml, exception handling, returns parsed file, chromosome number and LRG number from file

    try:
        tree = ET.parse(LRG_file) 
        
    except FileNotFoundError:
            print("File not found, please check name")
    except ParseError:
            print("LRG file not XML format! Please check file")

    root = tree.getroot()
    
    # Find the chromosome number - this is found under fixed annotation in XML.
    mapping = root.find("./updatable_annotation/annotation_set/mapping")
    chrom = mapping.get('other_name')
    chromosome='chr'+chrom
    
    # Get LRG ID number for adding to file name
    LRG_ID_num = root.find("./fixed_annotation/id").text
    
    return root, chromosome, LRG_ID_num

def getExons(root, Transcript):    
    
    # Gets exon start and finish points from LRG file: These are LRG specific values to be converted to genomic coordinates.

    # Find all the exons where the transcript name is equal to Transcript from parser argument to variable
    exons = root.findall(f"./fixed_annotation/transcript[@name='{Transcript}']/exon") 
     
    # For each exon in exon, set the start and end values for the first set of coordinates (LRG)
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

    # Converts LRG coordinates to genomic co-ordinates using genomic build from parser variable BuildName. 
    
    GenomicReference = root.find(f"./updatable_annotation/annotation_set/mapping[@coord_system='{BuildName}']/")
    
    # Find the strand 1 or -1 this will allow selection of correct figure to convert LRG coordinates to genome build coordinates
    
    assert ET.iselement(GenomicReference), 'Genome Build not found, please check build'
    
    Strand = int(GenomicReference.get('strand')) # Find strand number and store in variable. 

    if Strand == -1:
        otherstart = GenomicReference.get('other_end') # Selects other value if strande is = -1
        
        # Convert the value from string to int
        otherstartint = int(otherstart)
    
        # Convert lrg exon coordinates using 'other_end' into genome coords
        start_gen = [(otherstartint+1)-int(x) for x in start]
        end_gen = [(otherstartint+1)-int(x) for x in end]
        
        
    else: 
        otherstart = GenomicReference.get('other_start') # strand is = to 1
    
        # Convert the value from string to int
        otherstartint = int(otherstart)
    
        # Convert lrg exon coordinates using 'other_start' into genome coords
        start_gen = [int(x)+(otherstartint-1) for x in start]
        end_gen = [int(x)+(otherstartint-1) for x in end]
        
       
    #Tidy up the buildname so it can be used in the BedFile name for file creation
    genstring=BuildName[0:6] +'-' + BuildName[7:10]


    return genstring, start_gen, end_gen

def writeBedFile(LRG_ID_num, genstring, chromosome, start_gen, end_gen, Transcript):

    # Creating bed file using chromosome number, start and end genomic coordinates and strings genome build name and LRG ID for file creation

    bedfile = open(f'{LRG_ID_num}_{genstring}_{Transcript}.bed', "w") # Creates file
    
    bedfile.write("Chrom" + "\t" + "Start" + "\t" + "End" + "\n") 
    for i in range(len(start_gen)):
        bedfile.write(chromosome + "\t" + str(start_gen[i]) + "\t" + str(end_gen[i]) + "\n") # Adds chr name, start and end coordinates into tab seperated .bed file

    bedfile.close()

if __name__ == "__main__":
    main()
