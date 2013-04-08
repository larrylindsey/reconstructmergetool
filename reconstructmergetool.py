#  Files: reconstructmergetool.py, Series.py, Section.py, Transform.py,
#         Contour.py, ZContour.py, Image.py, ObjectList.py, xmlTree.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 4/8/2013
#
# Currently working on:
    #===== XML file creation (xmlOut)
        # Problems: Attribs out of order (use ordereddictionary),
        #           Outputting transform for every object rather than mult.
        #           objects within a single transform
        #           border,fill can be floats (Contour)
        # 1) read in section, write out section
        # 2) read in section, write out section with all dim = 0
        # 3) check if read similarly in reconstruct
    #===== ZContour: turn points into list of ints/floats/tuples rather than strings
    #===== Check comments/docstrings
import os, magic
from xmlTree import *
from Series import *
from Section import *

def main():
    inpath = '/home/michaelm/Documents/TestVolume/in/'
    outpath = '/home/michaelm/Documents/TestVolume/out/'
    
#SERIES
    #Make series object
    series = getser(inpath)

    
#SECTIONS
    #Make list of all section files in inpath
    secList = getsec(inpath)
    #Add all section objects to series object
    for sec in secList:
        print(sec)
        section = Section( xmlTree(inpath+sec) )
        series.addsection( section )
    print('Sections appended to series')


def getser(inpath):
    '''Searches <inpath> for a .ser file and returns a <series> object for that file'''
    print('Creating series...'),
    for file in os.listdir(inpath):
        if file.endswith('.ser'):
            tree = xmlTree(inpath+file)
            series = Series(tree)
    print('DONE')
    print('\tSeries: '+series._name)
    return series

def getsec(inpath):
    '''Searches <inpath> for section files and returns a list of all the sections'''
    print('Finding sections...'),
    secList = []
    count = 0
    for file in os.listdir(inpath):
        if 'XML' in str(magic.from_file(inpath+file)) and '.ser' not in file: #====
            secList.append( str(file) )
            count+=1
    print('DONE')
    print('\t%d sections found in %s'%(count,inpath))
    return secList

main()

# ==========================
# contour = section[1]
# print(contour.gettracepts())
# print(contour.getworldpts())
# 
# contour = section[2]
# print(contour.gettracepts())
# print(contour.getworldpts())
# 
# print(series.getattribs())
# 

