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
#  Date Last Modified: 6/7/2013
#
# Currently working on:
        # worldpts() needs dif for affine/polynomial
        # Series contours in mergeSerAtts, 
        # sections sorted in computer way (i.e. 12 after 111)
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
        series3 = mergeSeries(series, series2)
        #4)Output series file
        writeseries(series3, mergeoutpath)
        #5)Output section file(s)
        writesections(series3, mergeoutpath)
        
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

# === Problems with setidentzero() function & grouping under same transform
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
    if i.lower() in ['y', 'yes']:
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
    
def mergeSeries(serObj1, serObj2, name=None): #===
    '''Takes in two series objects and returns a 3rd, merged series object'''
    if name == None: # If not specified...
        name = serObj1.name #... output series will have same name as serObj1
        
    # Create output series object with merged attributes
    serObj3 = mergeSerAtts(serObj1, serObj2, name) # Merge series attributes
    serObj3.contours = mergeSerConts(serObj1, serObj2) # Merge series contours===

    # Populate shapely shapes in all contours for both series
    popshapes(serObj1)
    popshapes(serObj2)
    print('Done 3')
    
    # Create list of parallel section pairs (paired by section name)
    pairlist = [(x,y) for x in serObj1.sections for y in serObj2.sections if x.name.partition('.')[2] == y.name.partition('.')[2]  ]
    
    # Merge sections
    for (x,y) in pairlist:
        print(x.name+' '+y.name)
        serObj3.sections.append( mergeSections(x,y,name) )

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
#         print('==================================='+section.name+'====================================')
        for contour in section.contours:
            contour.popshape()
    print('DONE')
#             print(self.name) #===
    
def mergeSerAtts(ser1Obj, ser2Obj, ser3name):
    print('Mergeseratts')
    # Compare and merge series attributes from ser1Obj/ser2Obj
    ser1atts = ser1Obj.output()[0]
    ser2atts = ser2Obj.output()[0]
    ser3atts = {}
    for att in ser1atts:
        print(att)
        if ser1atts[att] == ser2atts[att]:
            ser3atts[att] = ser1atts[att]
        else:
            print('Series attributes do not match: '+str(att))
            print(ser1atts[att]+' '+ser2atts[att])
            a = 3
            while a not in [1,2]:
                a = int( raw_input('Choose attribute to pass to output series... 1 or 2: ') )
                if a == 1:
                    ser3atts[att] = ser1atts[att]
                elif a == 2:
                    ser3atts[att] = ser2atts[att]
                else:
                    print('Invalid choice. Please enter 1 or 2')
    # Create series object with merged attributes
    elem = ET.Element('Series')
    for att in ser3atts:
        elem.set( str(att), ser3atts[att] ) 
    series = Series(elem, ser3name)
    return series

def mergeSerConts(ser1Obj, ser2Obj): #=== 
    print('Mergeserconts')
    # Compare and merge series contours to new series ===
    ser1conts = ser1Obj.contours
    ser2conts = ser2Obj.contours
    ser3conts = ser1conts #=== TeMPORARY
    #=== compare all, present as choice
    #=== 
    
#     if len(ser1Obj.sections) == len(ser2Obj.sections):
#         for i in range(len(ser1Obj.sections)):
#             s = Section # Imgs? ===
    
    return ser3conts

def mergeSections(sec1, sec2, ser3name): #===
    '''compares and merges the attributes associated with Sections (except contours).
    i.e. imgs, index, thickness, alignLocked'''
    sec3 = Section()
    # Check index
    if sec1.index == sec2.index:
        sec3.index = sec1.index
        sec3.name = ser3name+'.'+str(sec3.index)
    # Check imgs
    if len(sec1.imgs) == len(sec1.imgs) and len(sec1.imgs) == 1: # If only 1 image and same name...
        if sec1.imgs[0].name == sec2.imgs[0].name:
            sec3.imgs = sec1.imgs
    elif len(sec1.imgs) != len(sec2.imgs) or len(sec1.imgs) != 1 or len(sec2.imgs) != 1: # If different # of imgs
        imgs1 = [image.src for image in sec1.imgs]
        imgs2 = [image.src for image in sec2.imgs]
        print('Different images present: '+'1.'+imgs1+' 2.'+imgs2)
        a = 3
        while a not in [1,2]:
            a = int(raw_input('Please pick which set of images to add to the merged section. 1 or 2: '))
            if a == 1:
                sec3.imgs = sec1.imgs
            elif a == 2:
                sec3.imgs = sec1.imgs
            else:
                print('Invalid choice. Please enter 1 or 2')
                a = int(raw_input('Please pick which set of images to add to the merged section. 1 or 2: '))
    # Check thickness
    if sec1.thickness == sec2.thickness:
        sec3.thickness = sec1.thickness
    elif sec1.thickness != sec2.thickness:
        print('Different thicknesses: '+'1.'+sec1.thickness+' 2.'+sec2.thickness)
        a = 3
        while a not in [1,2]:
            a = int(raw_input('Please pick which thickness to set to the merged section. 1 or 2: '))
            if a == 1:
                sec3.thickness = sec1.thickness
            elif a == 2:
                sec3.thickness = sec1.thickness
            else:
                print('Invalid choice. Please enter 1 or 2')
                a = int(raw_input('Please pick which thickness to set to the merged section. 1 or 2: '))
    # Check alignLocked
    if sec1.alignLocked == sec2.alignLocked:
        sec3.alignLocked = sec1.alignLocked
    elif sec1.alignLocked != sec2.alignLocked:
        print('Different thicknesses: '+'1.'+sec1.alignLocked+' 2.'+sec2.alignLocked)
        a = 3
        while a not in [1,2]:
            a = int(raw_input('Please pick which alignLocked to set to the merged section. 1 or 2: '))
            if a == 1:
                sec3.alignLocked = sec1.alignLocked
            elif a == 2:
                sec3.alignLocked = sec1.alignLocked
            else:
                print('Invalid choice. Please enter 1 or 2')
                a = int(raw_input('Please pick which alignLocked to set to the merged section. 1 or 2: '))
                
    #======================================================            
    # Build lists of contours for both sections
    conts1 = [contour for contour in sec1.contours]
    conts2 = [contour for contour in sec2.contours]

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
                if cont2.name == lst1[0].name: # Do they have same name?
                    if boxOverlaps(lst1[0], cont2): # Do the bounding boxes overlap?
                        lst2.append(cont2)
                        conts2.remove(cont2)
            
            # If no overlaps found, add lst1 contour to output list
            if len(lst2) == 0: 
                outputlist.append( lst1.pop() )
                
            # For each cont in lst2 (sec2 conts that overlap lst1 cont), ...
            # ...find overlaps in conts1 (unpopped [non lst1] sec1 contours)
            else:
                for contour2 in lst2:
                    for cont1 in conts1: # Original contour list for sec1
                        if cont1.name == contour2.name: # Do they have the same name?
                            if boxOverlaps(contour2, cont1): # Do the bouding boxes overlap?
                                lst1.append(cont1)
                                conts1.remove(cont1)
            
            # Bounding box overlaps have been found, now check actual polygons
            print([elem.name for elem in lst1])
            print([elem.name for elem in lst2])
            lstcnt = 0 # Problems with non-exist elems, use indexing/pop instead of remove()
            for elem in lst1: # Compare lst1 contours...
                lstcnt2 = 0
                for elem2 in lst2: # ... to lst2 contours
                    c = checkShape(elem, elem2)
                    if c == True: # Most likely to be same object
                        outputlist.append(elem)
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
    sec3.contours = outputlist

    return sec3
main()


