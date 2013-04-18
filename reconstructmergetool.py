#  Files: reconstructmergetool.py, Series.py, Section.py, Transform.py,
#         Contour.py, ZContour.py, Image.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 4/17/2013
#
# Currently working on:
    #===== XML file creation (xmlOut)
        # To do: 
        # 1) read in section, write out section
        # 2) read in section, write out section with all dim = 0
        # 3) check if read similarly in reconstruct
        
        # Problems:
        # 1) Series.py needs appropriate output format
        # 2) Default attributes to replace None type
        # 3) Newline characters?
import os,magic
from Series import *
from Section import *
#import xml.etree.ElementTree as ET
from lxml import etree as ET

def main():
    # = = = = = = = = = = = = = = = = = = = = =
    #Input/Output paths
    inpath = '/home/michaelm/Documents/TestVolume/testin/'
    outpath = '/home/michaelm/Documents/TestVolume/testout/'
    #inpath = '/home/wtrdrnkr/Documents/reconstructmergetool/References/'
    #outpath = inpath
    # = = = = = = = = = = = = = = = = = = = = =
    
    #1)Create series object
    series = getseries(inpath)
    #2)Append sections to series
    getsections(series, inpath)
    #3)Output series file
    writeseries(series, outpath)

# HELPER FUNCTIONS
def getseries(inpath):
    print('Creating series...'),
    #Get series path
    ser = ''
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

def writeseries(series, outpath):
    print('Writing series file...'),
    seriesoutpath = outpath+series._name+'.ser'
    #Build series root element
    attdict, contours = series.output()
    element = ET.Element(series._tag, attdict)
    #Build contour elements and append to root
    for contour in contours:
        element.append( ET.Element(contour._tag,contour.output()) )
    #Xml tree wrapper
    elemtree = ET.ElementTree(element)
    elemtree.write(seriesoutpath, pretty_print = True, xml_declaration=True, encoding="UTF-8")
    #ET.ElementTree(element).write(seriesoutpath)

    print('DONE')
    print('\tSeries output to: '+str(outpath+series._name+'.ser'))
    
main()

