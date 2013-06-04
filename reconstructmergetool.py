#  Files: reconstructmergetool.py, Series.py, Section.py, Transform.py,
#         Contour.py, ZContour.py, Image.py
#
#  Required Python libraries:
#        shapely, lxml, numpy, skimage
#  Other required libraries:
#        
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 6/4/2013
#
# Currently working on:
        # Run tests on volume josef, find problem contours (i.e. less than 3 pts for closed)
        # sections sorted in computer way (i.e. 12 after 111)
        # try merge w/ ident trans
        # Take in path instead of xmltree (series)?
            # ability to create empty series/sections (node or root == None)
        # Polynomial transforms
        # GUI: KIVY, WX(windows?), GTK, QT
        # tospace() fromspace() in transform

        
'''Merge two series together'''
import sys, os, re, math, time
from Series import *
from Section import *
from lxml import etree as ET
import PyQt4

if len(sys.argv) > 1:
    ser = os.path.basename(sys.argv[1]) #Name of series
    ser2 = os.path.basename(sys.argv[2]) 
    inpath = os.path.abspath(os.path.dirname(sys.argv[1]))+'/' #Directory of series
    inpath2 = os.path.abspath(os.path.dirname(sys.argv[2]))+'/'
    mergeoutpath = os.path.dirname(os.path.dirname(inpath))+'/merged/' #===

def main():
    if __name__ != '__main__':
        print('Welcome to reconstructmergetool')
        return
    if len(sys.argv) > 1:
        #1)Create series object
        series = getseries(inpath+ser)
        series2 = getseries(inpath2+ser2)
        #2)Append sections to series
        getsections(series, inpath+ser)
        getsections(series2, inpath2+ser2)
        #3)Merge series
        a = time.time() # Start time
        series3 = mergeSeries(series, series2)
        #4)Output series file
        writeseries(series3, mergeoutpath)
        #5)Output section file(s)
        writesections(series3, mergeoutpath)
        b = time.time() # End time
        c = b-a # Total time for merge
        print('Merge complete. Total time: '+str(c))
        
def getseries(path_to_series, name=None):
    print('Creating series object...'),
    #Parse series
    ser = os.path.basename(path_to_series)
    if name:
        ser = ser+'merge'
    serpath = os.path.dirname(path_to_series)+'/'+ser
    tree = ET.parse(serpath)
    
    root = tree.getroot() #Series
    #Create series object
    series = Series(root, ser.replace('.ser',''))
    print('DONE')
    print('\tSeries: '+series.name)
    return series

def writeseries(series_object, outpath):
    series = series_object
    print('Creating output directory...'),
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    print('DONE')
    print('\tCreated: '+outpath)
    print('Writing series file...'),
    seriesoutpath = outpath+series.name+'.ser'
    #Build series root element
    attdict, contours = series.output()
    root = ET.Element(series.tag, attdict)
    #Build contour elements and append to root
    for contour in contours:
        root.append( ET.Element(contour.tag,contour.output()) )

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
    print('\tSeries output to: '+str(outpath+series.name+'.ser'))

def getsections(series, path_to_series):
    #Build list of paths to sections
    print('Finding sections...'),
    ser = os.path.basename(path_to_series)
    inpath = os.path.dirname(path_to_series)+'/'
    serfixer = re.compile(re.escape('.ser'), re.IGNORECASE)
    sername = serfixer.sub('', ser)
    # look for files with 'seriesname'+'.'+'number'
    p = re.compile('^'+sername+'[.][0-9]*$')
    pathlist = [f for f in os.listdir(inpath) if p.match(f)] #list of paths to sections
    print('DONE')
    print('\t%d section(s) found in %s'%(len(pathlist),inpath))
    #Create and add section objects to series
    print('Creating section objects...'),
    for sec in pathlist:
        secpath = inpath + sec
        tree = ET.parse(secpath)
        root = tree.getroot() #Section
        section = Section(root,sec)
        series.addsection(section)
    series.sections = sorted(series.sections, key=lambda Section: Section.name) #sort by name
    print('DONE')

def writesections(series_object, outpath):
    series = series_object
    print('Writing section file(s)...'),
    
    count = 0
    for section in series.sections:
        sectionoutpath = outpath+section.name
        count += 1
        #Build section root element
        attdict = section.output()
        root = ET.Element(section.tag, attdict)
        
        for elem in section.contours:
            curT = ET.Element('Transform', elem.transform.output())
            
            #build list of transforms in root; check if transform already exists
            tlist=[]
            for trnsfrm in root.getchildren():
                tlist.append(trnsfrm.attrib)

            # Image/Image contour transform
            if elem.img: # Make transform from image
                if elem.transform.output() == section.imgs[0].transform.output():
                    subelem = ET.Element('Image', section.imgs[0].output())
                    curT.append(subelem)
                    subelem = ET.Element(elem.tag, elem.output())
                    curT.append(subelem)
                    root.append(curT)

# === Problems with setidentzero() function
#                 else:
#                     print(elem.name),
#                     print(elem.transform.output()) #===
#                     
#                     print( section.imgs[0].transform.output() ) #===
#                     print('Error: Image transform does not match contour transform '+'('+str(section.name)+')')
                
            # Transform already exist === Issues grouping under img transform
            #elif curT.attrib in tlist:
            #    for trnsfrm in root.getchildren():
            #        if curT.attrib == trnsfrm.attrib:
            #            subelem = ET.Element(elem.tag, elem.output())
            #            trnsfrm.append(subelem)
            # New transform   
            else:
                subelem = ET.Element(elem.tag, elem.output())
                curT.append(subelem)
                root.append(curT)
        
        elemtree = ET.ElementTree(root)
        elemtree.write(sectionoutpath, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    print('DONE')
    print('\t%d Section(s) output to: '+str(outpath))%count

def setidentzero(serObj):
    '''Converts points for all sections in a series to identity transform'''
    i = raw_input('setidentzero() will PERMANENTLY alter data in '+serObj.name+'... Continue? y/n  ')
    if i in ['y', 'Y', 'yes', 'Yes']:
        print('Converting sections...'),
        series = serObj
        for sec in series.sections:
            for c in sec.contours:
                if not c.img:
                    c.points = c.transform.worldpts(c.points)
                    c.transform.dim = 0
                    c.transform.ycoef = [0,0,1,0,0,0]
                    c.transform.xcoef = [0,1,0,0,0,0]
                    c._tform = c.transform.poptform()
        print('DONE')
    else:
        return 'Abort...'
    
def mergeSeries(serObj1, serObj2):
    '''Takes in two series objects and outputs a 3rd series object with merged contours'''

    # Create output series/sections === copy vals from ser1, later merge vals
    serObj3 = getseries(inpath+ser)
    #=== serObj3 = Series()
    #=== ser3AttList = mergeSerAtt(serObj1, serObj2)
    getsections(serObj3, inpath+ser) #=== remove?
        
    # Populate shapely shapes in all contours for both series
    popshapes(serObj1)
    popshapes(serObj2)

    # Create list of parallel section pairs (paired by section name)
    pairlist = [(x,y) for x in serObj1.sections for y in serObj2.sections if x.name.partition('.')[2] == y.name.partition('.')[2]  ]
    
    count = 0 # Keep track of current section
    for secPair in pairlist: # For each section pair
        print(secPair[0].name+' '+secPair[1].name) # Print parallel section names

        # Build lists of contours for both sections
        conts1 = [contour for contour in secPair[0].contours]
        conts2 = [contour for contour in secPair[1].contours]

        outputlist = [] # List of all contours to be output into 3rd series
        
        # Find overlapping contours
        while len(conts1) != 0 and len(conts2) != 0: # Continue until either list is empty
            # Find overlaps in conts2 for each contour in conts1
            for cont in conts1:
                lst1 = [conts1.pop()] # Conts1 contour
                print('Checking: '+lst1[0].name)
                # Find overlaps in conts2
                lst2 = [] # All the conts2 contours that overlap with the lst1 contour
                for cont2 in conts2:
#                     print('    Check against: '+cont2.name)
                    if cont2.name == lst1[0].name: # Do they have same name?
                        if boxOverlaps(lst1[0], cont2): # Do the bounding boxes overlap?
#                             print('boxOverlaps() 1')
                            lst2.append(cont2)
                            conts2.remove(cont2)
                
                # If no overlaps found, add lst1 contour to output list
                if len(lst2) == 0: 
                    outputlist.append( lst1.pop() )
                # For each cont in lst2 (overlaps in sec2), find overlaps in conts1 (unpopped sec1 contours)
                else:
                    for contour2 in lst2:
                        for cont1 in conts1: # Original contour list for sec1
                            if cont1.name == contour2.name: # Do they have the same name?
                                if boxOverlaps(contour2, cont1): # Do the bouding boxes overlap?
#                                     print('boxOverlaps() 2')
                                    lst1.append(cont1)
                                    conts1.remove(cont1)
                
                # Bounding box overlaps have been found, now check actual polygons
                print([elem.name for elem in lst1])
                print([elem.name for elem in lst2])
                lstcnt = 0 #=== problems with non-exist elems, use indexing/pop instead of remove()
                for elem in lst1: # Compare lst1 contours...
                    lstcnt2 = 0
                    for elem2 in lst2: # ... to lst2 contours
                        c = checkShape(elem, elem2)
#                         print('chkshpe')
                        if c == True: # Most likely to be same object
                            print(len(outputlist))
                            outputlist.append(elem)
                            print(len(outputlist))
                            lst1.pop(lstcnt)
                            lst2.pop(lstcnt2)
            
                        elif c == 1: # Different traces with same name
                            a = raw_input('Choose trace to output: '+'1. sec1\n'+'2, sec2') #=== User input or no?
                            if int(a) == 1:
                                outputlist.append(elem)
                            if int(a) == 2:
                                outputlist.append(elem2)
                            else:
                                print('Invalid option...')  
                                lst1.pop(lstcnt)
                                lst2.pop(lstcnt2)
#===                         else:
#                             a = raw_input('check: '+elem.name+' '+elem2.name)
                        lstcnt2+=1
                    lstcnt+=1
                print
                
        # Add leftover contours (from conts1/conts2) to output list
        # Left overs mean they have no matching/overlapping contours in parallel section
        print('leftover conts1: '+str([elem.name for elem in conts1]))
        while len(conts1) != 0:
            outputlist.append( conts1.pop() )
        print('leftover conts2: '+str([elem.name for elem in conts2]))
        while len(conts2) != 0:
            outputlist.append( conts2.pop() )
        print('Output: '+str([elem.name for elem in outputlist]))

        
        # Add output contours to section.contours list
        serObj3.sections[count].contours = outputlist
        count += 1
        print
    return serObj3

def boxOverlaps(cont1, cont2):
    '''Determines if there is an overlap between the shape bounding boxes.
    Returns True if there is overlap, otherwise false.'''
    if cont1._shape == None or cont2._shape == None:
        return False
#     elif cont1.img == True or cont2.img == True: #===
#         print('Image, ignore: '+cont1.name+' '+cont2.name)
#         return False
    elif cont1.box().intersects( cont2.box() ) or cont1.box().touches( cont2.box() ):
        print('Bounding box overlap: '+cont1.name+' '+cont2.name)
        return True
    else:
        return False  
    
def checkShape(cont1, cont2): #===
    '''Handles LineString and Polygons separately.
    For Polygons:
    For LineStrings:
    '''
    # CLOSED TRACES
    if cont1.closed == True and cont2.closed == True:
        AoU = cont1._shape.union( cont2._shape ).area # Area of union
        AoI = cont1._shape.intersection( cont2._shape ).area # Area of intersection
        
        # Overlap is near 100%
        if AoI != 0.0 and AoU/AoI < (1+2**(-17)):
            print('    Polygon overlap near 100')
            return True

        # AoI is zero, no overlap
        elif AoI == 0.0:
            print('    Polygons do not overlap')
            return False
        
        # Some overlap
        elif AoI != 0.0:
            print('    Overlap exists, not near 100 PLACE HOLDER: USER INPUT') #=== Place holder for user input
            return 1

    # OPEN TRACES===     
    elif cont1.closed == False and cont2.closed == False: #===
        print('    Open trace')  
    
    # UNKNOWN ERROR===
    else:
        print('    Unknown Trace Type')

def popshapes(serObj):
    print('Populating shapely shapes for '+serObj.name+'...'),
    for section in serObj.sections:
        print('==================================='+section.name+'====================================')
        for contour in section.contours:
            contour.popshape()
    print('DONE')
    
main()


