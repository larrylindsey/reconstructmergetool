#  Files: reconstructmergetool.py, Series.py, Section.py, Transform.py,
#         Contour.py, ZContour.py, Image.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 4/24/2013
#
# Currently working on:
    #===== XML file creation (xmlOut)
        # To do: 
        # 1) read in section, write out section
        # 2) read in section, write out section with all dim = 0
        
        # Problems: #===
        # 1) Get rid of transform objects in seclist, rework XML output: if transform == prevtransform: etc
        # 2) method of reading files, determine section files from series name

import os,magic
from Series import *
from Section import *
from lxml import etree as ET
def test():
    inpath = '/home/michaelm/Documents/TestVolume/testin/Volumejosef.99'
    outpath = '/home/michaelm/Documents/TestVolume/testout/'
    tree = ET.parse(inpath)
    root = tree.getroot()
    section = Section(root, 'Volumejosef.99')
    print(section._list)
    for i in section._list:
        if i._tag == 'Contour':
            print(i._img)

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
    #4)Output section file(s)
    writesections(series, outpath)
    
    
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
    root = ET.Element(series._tag, attdict)
    #Build contour elements and append to root
    for contour in contours:
        root.append( ET.Element(contour._tag,contour.output()) )
    #Xml tree wrapper
    elemtree = ET.ElementTree(root)
    elemtree.write(seriesoutpath, pretty_print = True, xml_declaration=True, encoding="UTF-8")
    print('DONE')
    print('\tSeries output to: '+str(outpath+series._name+'.ser'))

def writesections(series, outpath): #===
    print('Writing section file(s)...'),
    
    count = 0
    for section in series._sections:
        sectionoutpath = outpath+section._name
        count += 1
        #Build section root element
        attdict = section.output()
        root = ET.Element(section._tag, attdict)
        
        #===
        curT = 'current transform'
        for elem in section._list:
            #If transform, make element and append to root
            if elem._tag == 'Transform':
                tmpT = ET.Element(elem._tag, elem.output())
                if curT == 'current transform':
                    curT = tmpT
                #elif  tmpT != curT:
                else:
                    root.append(curT)
                    curT = tmpT
            #If not transform make element and append to transform
            else:
                subelem = ET.Element(elem._tag, elem.output())
                curT.append(subelem)
        root.append(curT)
        elemtree = ET.ElementTree(root)
        elemtree.write(sectionoutpath, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    print('DONE')
    print('\t%d Section(s) output to: '+str(outpath))%count
#main()
test()

