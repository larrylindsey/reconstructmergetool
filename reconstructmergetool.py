#  Files: reconstructmergetool.py, Series.py, Section.py, Transform.py,
#         Contour.py, ZContour.py, Image.py, ObjectList.py, xmlTree.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 4/16/2013
#
# Currently working on:
    #===== XML file creation (xmlOut)
        # To do: 
        # 1) read in section, write out section
        # 2) read in section, write out section with all dim = 0
        # 3) check if read similarly in reconstruct
        
        # Problems:
        # 1) Series attributes may not be correct (string, bools, lists)
        # 2) Check output for xml, especially booleans/lists
        # 3) xmlOut.py probably obsolete, keep in case
import os,magic
from Series import *
from Section import *
import xml.etree.ElementTree as ET

def main():
    # = = = = = = = = = = = = = = = = = = = = =
    #Folder containing series and section files
    inpath = '/home/michaelm/Documents/TestVolume/testin/'
    outpath = 'home/michaelm/Documents/TestVolume/testout/'
    # = = = = = = = = = = = = = = = = = = = = =
    #1)Create series object
    series = getseries(inpath)
    #2)Append sections to series
    getsections(series, inpath)
    #3)Write series files
    series.output(outpath)
    
    
    
    
    
    
    
    
    # === TESTING ===
#     print('Series contours')
#     for contour in series._contours:
#         print(contour)
#     print('\nSections & stuff')
#     for section in series._sections:
#         print(section)
#         for elem in section._list:
#             print(elem._tag)
    
    
# HELPER FUNCTIONS
def getseries(inpath):
    print('Creating series...'),
    ser = ''
    #Get series path
    for file in os.listdir(inpath):
        if file.endswith('.ser'):
            ser = str(file)
    #Parse series
    serpath = inpath + ser
    tree = ET.parse(serpath)
    root = tree.getroot() #Series
    
    #Create series object
    series = Series(root, ser.replace('.ser',''))
    print('DONE')
    print('\tSeries: '+series._name)
    return series

def getsections(series, inpath):
    #Build list of paths to sections
    print('Finding sections...'),
    pathlist = []
    count = 0
    for file in os.listdir(inpath):
        if 'XML' in str(magic.from_file(inpath+file)) and '.ser' not in file:
            pathlist.append( str(file) )
            count+=1
    print('DONE')
    print('\t%d section(s) found in %s'%(count,inpath))
    
    #Create and add section objects to series
    print('Creating section objects...'),
    for sec in pathlist:
        secpath = inpath + sec
        tree = ET.parse(secpath)
        root = tree.getroot() #Section
        section = Section(root,sec)
        series.addsection(section)
    print('DONE')

    
main()






















    

def poo(): 
    return
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

