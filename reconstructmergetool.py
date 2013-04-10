#  Files: reconstructmergetool.py, Series.py, Section.py, Transform.py,
#         Contour.py, ZContour.py, Image.py, ObjectList.py, xmlTree.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 4/10/2013
#
# Currently working on:
    #===== XML file creation (xmlOut)
        # Problems: Attribs out of order (use ordereddictionary),
        #           outputting None (e.g. .ser Contour hidden/simplified attributes)
        #            ^ attribs list in all objects? xmlOut.getattribs()
        #           Image has own contour within single transsform
        # 1) read in section, write out section
        # 2) read in section, write out section with all dim = 0
        # 3) check if read similarly in reconstruct
    #===== ZContour: turn points into list of ints/floats/tuples rather than strings
    #===== Check comments/docstrings
import os, magic, xmlOut
from xmlTree import *
from Series import *
from Section import *

def main():
    inpath = '/home/michaelm/Documents/TestVolume/testin/'
    outpath = '/home/michaelm/Documents/TestVolume/testout/'
    
#SERIES
    #Make series object
    series = getser(inpath)
    
#SECTIONS
    #Make list of all section files in inpath
    secList = getsec(inpath)
    #Add all section objects to series object
    for sec in secList:
        section = Section( xmlTree(inpath+sec) )
        series.addsection( section )
    print('Section(s) appended to Series: %s'%series._name)

#WRITE OUT
    #Series
    print('Writing series file...'),
    #rawlist = xmlOut.outseries(series)
    #xmlOut.output(rawlist, outpath+series._name, 'ser')
    print('DONE')
    
    #Sections
    print('Writing section file(s)...'),
    for sec in series._list:   
        rawlist = xmlOut.outsection(sec)
        xmlOut.output(rawlist, outpath+sec._name, 'xml')
    print('DONE')
    print('\tFiles placed in: %s'%outpath)

# HELPER FUNCTIONS
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
    print('\t%d section(s) found in %s'%(count,inpath))
    return secList

main()
