#  Files: reconstructmergetool.py, Series.py, Section.py, Transform.py,
#         Contour.py, ZContour.py, Image.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 5/16/2013
#
# Currently working on:
        # 1) read in section, write out section with all dim = 0 (def setidentzero())
        # 2) phase out magic, use regular expressions
        # 3) Polynomial transforms
        # 4) tospace() fromspace() in transform
        
        # Issues:
        # 1) Image trans assumes not like others (commented out the common transform compression)
        # 2) PyDev console not using updated reconstructmergetool.py
        # 3) ZContours have no transform
        
'''Reconstructmergetool - Merge two series together'''
import sys, os, re
from Series import *
from Section import *
from lxml import etree as ET

if len(sys.argv) > 1:
    ser = os.path.basename(sys.argv[1])
    inpath = os.path.dirname(sys.argv[1])+'/'
    outpath = inpath+'rmt/'

def main():
    if __name__ != '__main__':
        return
    if len(sys.argv) > 1:
        #1)Create series object
        series = getseries(inpath+ser)
        #2)Append sections to series
        getsections(series)
        #3)Output series file
        writeseries(series, outpath)
        #4)Output section file(s)
        writesections(series, outpath)
    else:
        print('Welcome to reconstructmergetool')
        print('To create a series, use the function series = getseries(<path>)')
        print('Next, find sections using getsections(series)')
        print('To write the series file(s), use writeseries(series, <outpath>')
        print('Finally, to write the section file(s), use writesections(series, <outpath>)')

def getseries(inpath):
    print('Creating series...'),
    #Parse series
    ser = os.path.basename(inpath)
    serpath = os.path.dirname(inpath)+'/'+ser
    tree = ET.parse(serpath)

    root = tree.getroot() #Series
    #Create series object
    series = Series(root, ser.replace('.ser',''))
    print('DONE')
    print('\tSeries: '+series._name)
    return series

def writeseries(series, outpath):
    print('Creating output directory...'),
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    print('DONE')
    print('\tCreated: '+outpath)
    print('Writing series file...'),
    seriesoutpath = outpath+series._name+'.ser'
    #Build series root element
    attdict, contours = series.output()
    root = ET.Element(series._tag, attdict)
    #Build contour elements and append to root
    for contour in contours:
        root.append( ET.Element(contour._tag,contour.output()) )

    strlist = ET.tostringlist(root)
    # Needs to be in order: hideTraces/unhideTraces/hideDomains/unhideDomains
        # Fix order:
    strlist = strlist[0].split(' ') # Separate single string into multple strings for each elem
    count = 0
    for elem in strlist:
        if 'hideTraces' in elem and 'unhideTraces' not in elem:
            strlist.insert(1, strlist.pop(count))
        count += 1
    count = 0
    for elem in strlist:
        if 'unhideTraces' in elem:
            strlist.insert(2, strlist.pop(count))
        count += 1
    count = 0
    for elem in strlist:
        if 'hideDomains' in elem and 'unhideDomains' not in elem:
            strlist.insert(3, strlist.pop(count))
        count += 1
    count = 0
    for elem in strlist:
        if 'unhideDomains' in elem:
            strlist.insert(4, strlist.pop(count))
        count += 1
        # Recombine into list of single str
    tempstr = ''
    for elem in strlist:
        tempstr += elem + ' '
    strlist = []
    strlist.append( tempstr.rstrip(' ') ) # Removes last blank space

    # Write to .ser file
    f = open(seriesoutpath, 'w')
    f.write('<?xml version="1.0"?>\n')
    f.write('<!DOCTYPE Section SYSTEM "series.dtd">\n\n')
    for elem in strlist:
        if '>' not in elem:
            f.write(elem),
        else:
            elem = elem+'\n'
            f.write(elem)
            if '/' in elem:
                f.write('\n')        
        
#!!!!!!!!! ===    Removed for keeping hide/unhide traces/domains in order
#     #Xml tree wrapper
#     elemtree = ET.ElementTree(root)
#     elemtree.write(seriesoutpath, pretty_print = True, xml_declaration=True, encoding="UTF-8")
    print('DONE')
    print('\tSeries output to: '+str(outpath+series._name+'.ser'))

def getsections(series):
    #Build list of paths to sections
    print('Finding sections...'),
    serfixer = re.compile(re.escape('.ser'), re.IGNORECASE)
    sername = serfixer.sub('', ser)
    # look for files with 'seriesname'+'.'+'number'
    p = re.compile('^'+sername+'[.][0-9]*$')
    pathlist = [f for f in os.listdir(inpath) if p.match(f)]
    print('DONE')
    print('\t%d section(s) found in %s'%(len(pathlist),inpath))
    #Create and add section objects to series
    print('Creating section objects...'),
    for sec in pathlist:
        secpath = inpath + sec
        #print(secpath)
        tree = ET.parse(secpath)
        root = tree.getroot() #Section
        section = Section(root,sec)
        series.addsection(section)
    print('DONE')

def writesections(series, outpath):
    print('Writing section file(s)...'),
    
    count = 0
    for section in series._sections:
        sectionoutpath = outpath+section._name
        count += 1
        #Build section root element
        attdict = section.output()
        root = ET.Element(section._tag, attdict)
        
        for elem in section._list:
            curT = ET.Element('Transform', elem._transform.output())
            
            #build list of transforms in root; check if transform already exists
            tlist=[]
            for trnsfrm in root.getchildren():
                tlist.append(trnsfrm.attrib)

            # Image/Image contour transform
            if elem._img: # Make transform from image
                if elem._transform.output() == section._imgs[0]._transform.output():
                    subelem = ET.Element('Image', section._imgs[0].output())
                    curT.append(subelem)
                    subelem = ET.Element(elem._tag, elem.output())
                    curT.append(subelem)
                    root.append(curT)
                else:
                    print(elem._name),
                    print(elem._transform.output()) #===
                    
                    print( section._imgs[0]._transform.output() ) #===
                    print('Error: Image transform does not match contour transform '+'('+str(section._name)+')')
                
            # Transform already exist === Issues grouping under img transform
            #elif curT.attrib in tlist:
            #    for trnsfrm in root.getchildren():
            #        if curT.attrib == trnsfrm.attrib:
            #            subelem = ET.Element(elem._tag, elem.output())
            #            trnsfrm.append(subelem)
            # New transform   
            else:
                subelem = ET.Element(elem._tag, elem.output())
                curT.append(subelem)
                root.append(curT)
        
        elemtree = ET.ElementTree(root)
        elemtree.write(sectionoutpath, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    print('DONE')
    print('\t%d Section(s) output to: '+str(outpath))%count
def setidentzero(inpath):
    series = getseries(inpath)
    print('Converting series...'),
    for cont in series._contours:
        print(cont)
main()


