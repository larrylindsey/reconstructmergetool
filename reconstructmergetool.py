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
#  Date Last Modified: 5/23/2013
#
# Currently working on: 
        # Check if identical, two series (ident trans, and norm trans) -> merge 2 to single output
        # Polynomial transforms
        # tospace() fromspace() in transform
        # polygon in contour

        
'''Merge two series together'''
import sys, os, re, math
from Series import *
from Section import *
from lxml import etree as ET


if len(sys.argv) > 1:
    ser = os.path.basename(sys.argv[1]) #Name of series
    ser2 = os.path.basename(sys.argv[2]) 
    inpath = os.path.dirname(sys.argv[1])+'/' #Directory of series
    inpath2 = os.path.dirname(sys.argv[2])+'/'
    outpath = inpath+'rmt/' #=== #Output directory of series
    outpath2 = inpath2+'rmt2/' #===
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
        series3 = mergeSeries(series, series2)
#         #3)Output series file
#         writeseries(series, mergeoutpath)
#         writeseries(series2, mergeoutpath)
#         #4)Output section file(s)
#         writesections(series, mergeoutpath)
#         writesections(series2, mergeoutpath)

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
    '''Converts points for all sections in a series to identity trans'''
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
    
def mergeSeries(serObj1, serObj2, outpath=None):
    '''Takes in two series objects and outputs a 3rd, merged series object'''
    if not outpath: #optional output path parameter
        outpath = '/home/michaelm/Documents/TestVolume/merged/'
    
    serObj3 = getseries(inpath+ser) #=== copy vals from ser1, later merge vals
    
    # Populate shapely shapes in all contours
    popshapes(serObj1)
    popshapes(serObj2)

    # Create list of section pairs
    pairlist = [(x,y) for x in serObj1.sections for y in serObj2.sections if x.name.partition('.')[2] == y.name.partition('.')[2]  ]
         
    for pair in pairlist:
        print()
        print(pair[0].name+' '+pair[1].name) #===
        # Build lists of contours
        conts1 = [contour for contour in pair[0].contours]
        conts2 = [contour for contour in pair[1].contours]
        # Compare contours
        overlaps = [] # collection of overlap groups
        for cont in conts1:
            ovlpGrp = [] # Tuples containing overlapping contours
            for cont2 in conts2:
                if boxOverlaps(cont, cont2): #=== If fail, deeper analysis 
                    if difShape(cont, cont2):
                        ovlpGrp.append( tuple([cont,cont2]) )
            overlaps.append(ovlpGrp)
        #print(overlaps)
    
def boxOverlaps(cont1, cont2):
    '''Determines if there is an overlap between the shape bounding boxes.
    Returns True if there is overlap, otherwise false.'''
    if cont1._shape == None or cont2._shape == None:
        print('No shape: '+cont1.name+' '+cont2.name)
        return False
    elif cont1.box().intersects(cont2.box()) or cont1.box().touches(cont2.box()):
        return True
    else:
        return False  
    
def difShape(cont1, cont2):
    '''Handles LineString and Polygons separately.
    For Polygons: returns True if area of union/area of intersection is >= 1+2**(-17)
    For LineStrings: returns True if...................................''' #===
    # Closed traces
    if cont1.closed == True and cont2.closed == True:
        AoU = cont1._shape.union(cont2._shape).area # Area of union
        AoI = cont1._shape.intersection(cont2._shape).area # Area of intersection
        # Overlap is near 100%
        if AoI != 0.0 and AoU/AoI < (1+2**(-17)):
            print('Overlap near 100: '+cont1.name+' '+cont2.name) #===
            return False
        # AoI is zero, no overlap
        elif AoI == 0.0:
            print('Polygons no overlap, boxes do: '+cont1.name+' '+cont2.name)
        # Overlap not near 100%
        else: #=== user input?
            print('User input req: '+cont1.name+' '+cont2.name) #===
            return True
    
    # Open traces    
    elif cont1.closed == False and cont2.closed == False:
        print('LineString: '+cont1.name+' '+cont2.name) #===
    
    # Unknown error
    else:
        print('Error: '+cont1.name+' '+cont2.name)
        
        #=== Compare LineString (open traces)
#         for i in range(len(open1)):
#             if open1[i].length == open2[i].length:
#                 print('Same length '+str(open1[i].length)) #===
#             else:
#                 print(str(open1[i].length)+' '+str(open2[i].length)) #===
    
def popshapes(serObj):
    print('Populating shapely shapes for '+serObj.name+'...'),
    for section in serObj.sections:
        for contour in section.contours:
            contour.popshape()
    print('DONE')
    


main()


