import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-l', '--LRG', required=True, dest="LRG_File", help='The LRG xml file to be processed')
parser.add_argument('-b', '--Build', default='GRCh37.p13', dest="BuildName", help='Human genome build to use')
parser.add_argument('-t', '--Transcript', default='t1', dest="Transcript", help='Which LRG transcript to use')

results = parser.parse_args()
print('LRG: ',results.LRG_File) 
print('Build:', results.BuildName)
print('Transcript:', results.Transcript)
