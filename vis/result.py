#!/usr/bin/python

import sys, getopt

def main(argv):
   inputfile = ''
   caption = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('test.py -i <inputfile> -o <caption>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <inputfile> -o <caption>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         caption = arg
   print ('Input file is "', inputfile)
   print ('Output file is "', caption)

if __name__ == "__main__":
   main(sys.argv[1:])