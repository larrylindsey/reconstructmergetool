#  Files: reconstructmergetool.py, Series.py, Section.py, Transform.py,
#         Contour.py, ZContour.py, Image.py
#
#  Required Python libraries:
#        shapely, lxml, numpy, skimage
#  Other required libraries:
#        libgeo_c? 
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 6/19/2013
#
# Currently working on:
        # Make list of conflicts
        # Series contours in mergeSerAtts
        # sections sorted in computer way(? lol) (i.e. 12 after 111)
        # GUI: PySide
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
            tlist= [trnsfrm.attrib for trnsfrm in root.getchildren()]

            # Image/Image contour transform
            if elem.img != None: # Make transform from image
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
                c.points = c.transform.worldpts(c.points)
                c.transform.dim = 0
                c.transform.ycoef = [0,0,1,0,0,0]
                c.transform.xcoef = [0,1,0,0,0,0]
                c._tform = c.transform.poptform()
        print('DONE')
    else:
        return 'Abort...'
def mergeSeries(serObj1, serObj2, name=None):
    '''Takes in two series objects and returns a 3rd, merged series object'''
    if name == None: # If not specified...
        name = serObj1.name #... output series will have same name as serObj1
        
    # Create output series object with merged attributes
    serObj3 = mergeSerAtts(serObj1, serObj2, name) # Merge series attributes
    serObj3.contours = mergeSerConts(serObj1, serObj2) # Merge series contours===

    # Populate shapely shapes in all contours for both series
    popshapes(serObj1)
    popshapes(serObj2)
    
    # Create list of parallel section pairs (paired by section name)
    pairlist = [(x,y) for x in serObj1.sections for y in serObj2.sections if x.name.partition('.')[2] == y.name.partition('.')[2]  ]
    
    # Merge sections
    print('Merging Sections...'),
    for (x,y) in pairlist:
#         print('========'+x.name+' '+y.name+'========')
        serObj3.sections.append( mergeSections(x,y,name) )
    print('DONE')
    return serObj3
def popshapes(serObj):
    print('Populating shapely shapes for '+serObj.name+'...'),
    for section in serObj.sections:
#         print('========='+section.name+'=========')
        for contour in section.contours:
#             print(contour.name)
            contour.popshape() # Uses worldpts to create shapely shapes
    print('DONE') 
def mergeSerAtts(ser1Obj, ser2Obj, ser3name):
    print('Merging Series Attributes...'),
    # Compare and merge series attributes from ser1Obj/ser2Obj
    ser1atts = ser1Obj.output()[0] # Dictionary of attributes
    ser2atts = ser2Obj.output()[0] # "
    ser3atts = {}
    for att in ser1atts:
#         if att == 'viewport':
#             ser3atts[att] = '0.0 0.0 0.0'
#         elif att == 'index':
#             ser3atts[att] = '1'
        if ser1atts[att] == ser2atts[att]:
            ser3atts[att] = ser1atts[att]
        else:
            print('\nSeries attributes do not match: '+str(att))
            print('1: '+ser1atts[att]+'\n'+'2: '+ser2atts[att])
            a = 3
            while a not in [1,2]:
                a = int(raw_input('Choose attribute to pass to output series... 1 or 2: '))
                if a == 1:
                    ser3atts[att] = ser1atts[att]
                elif a == 2:
                    ser3atts[att] = ser2atts[att]
                else:
                    print('Invalid choice. Please enter 1 or 2')
            print
    # Create series object with merged attributes
    elem = ET.Element('Series')
    for att in ser3atts:
        elem.set( str(att), ser3atts[att] )
    series = Series(elem, ser3name)
    print('DONE')
    return series
def mergeSerConts(ser1Obj, ser2Obj): #=== currently copies ser1Obj.contours
    print('Merging Series Contours...'),
    # Compare and merge series contours to new series ===
    ser1conts = ser1Obj.contours
    ser2conts = ser2Obj.contours
    ser3conts = ser1conts #=== TEMPORARY
    #=== compare all, present as choice
    #=== 
    
#     if len(ser1Obj.sections) == len(ser2Obj.sections):
#         for i in range(len(ser1Obj.sections)):
#             s = Section # Imgs? ===
    print('DONE')
    return ser3conts
def chkCollision(lst1, lst2): #=== in dev, overlap outputs both
    '''Takes in two lists of contours, returns 1 list of contours'''
    threshold = (1+2**(-17))
    outlist = []
    for elem1 in lst1:
        for elem2 in lst2:
            # Closed traces
            if elem1.closed and elem2.closed:
                AoU = elem1._shape.union( elem2._shape ).area # Area of union
                AoI = elem1._shape.intersection( elem2._shape ).area # Area of intersection
                # Overlap is near 100%
                if AoU/AoI < threshold: # most likely the same object
                    outlist.append(elem1)
                    lst1.remove(elem1)
                    lst2.remove(elem2)
                # Some overlap
                elif AoI != 0.0: # require user input === output both for now
                    print(elem1.name +' '+elem2.name)
                    outlist.append(elem1)
                    outlist.append(elem2)
                    lst1.remove(elem1)
                    lst2.remove(elem2)
                    a = raw_input('chkCollision dbug')

            # Open traces
            elif not elem1.closed and not elem2.closed:
                # equivalency established in chkOvlp() ===
                outlist.append(elem1)
                lst1.remove(elem1)
                lst2.remove(elem2)
    return outlist

def mergeSections(sec1, sec2, ser3name):
    '''compares and merges the attributes associated with Sections (except contours).
    i.e. imgs, index, thickness, alignLocked'''
    # create section for merge
    sec3 = mergeSecAtts(sec1, sec2, chkSecAtts(sec1,sec2)) #===
    # check section images
    sec3.imgs = chkSecImgs(sec1,sec2)
    # chkContOvlps
    sec3.contours = chkContOvlps(sec1, sec2)
    return sec3
def chkSecAtts(sec1, sec2):
    '''Returns a list of booleans signifying whether attributes of sec1 and sec2 are the same'''
    chkDict = {}
    # chk attributes
    s1atts = sec1.output()
    s2atts = sec2.output()
    for att in s1atts:
        chkDict[att] = (s1atts[att] == s2atts[att])
    return chkDict
def mergeSecAtts(sec1, sec2, chkDict): #=== currently copies sec1.output()
    s1atts = sec1.output()
    s2atts = sec2.output()
    s3atts = {}
    for att in chkDict:
        if not chkDict[att]:
            a = raw_input('CONFLICT: mergeSecAtts') #===
            if a == 1:
                s3atts[att] = s1atts[att]
            else:
                s3atts[att] = s2atts[att]
        else:
            s3atts[att] = s1atts[att]
    elem = ET.Element('Section')
    for att in s3atts:
        elem.set(str(att), s3atts[att])
    sec3 = Section(elem, sec1.name) #=== sec1 name?
    return sec3
def chkSecImgs(s1, s2): #===
    '''Returns imgs to be addeded to new section'''
    if len(s1.imgs) != len(s2.imgs):
        return mergeSecImgs(s1,s2)
    for i in range( len(s1.imgs) ):
        if s1.imgs[i].output() != s2.imgs[i].output():
            return mergeSecImgs(s1,s2)
    return s1.imgs
def mergeSecImgs(s1,s2): #=== currently copies s1.imgs
    return s1.imgs
def chkContOvlps(s1, s2): #===
    '''Returns list of contours to be added to a merged section'''
    # Lists of all contours in parallel sections
    conts1 = [cont for cont in s1.contours]
    conts2 = [cont for cont in s2.contours]
    conts3 = []
    
    while len(conts1) != 0 and len(conts2) != 0:
        ovlp1 = [conts1.pop()]
        ovlp2 = []
        # Check sec2 for conts that ovlp with ovlp1
        print('1st pass:')
        print('Check: '+ovlp1[0].name)
        for cont in conts2:
            print(cont.name)
            if chkOvlp(ovlp1[0], cont):
                ovlp2.append(cont)
                conts2.remove(cont)
        # If no ovlps found, output contour to s3
        if not len(ovlp2):
            conts3.append(ovlp1[0])
        # Now find overlaps in s1 that ovlp with ovlp2 conts
        for cont in ovlp2:
            for cont2 in conts1:
                if chkOvlp(cont, cont2):
                    ovlp1.append(cont2)
                    conts1.remove(cont2)
        # Further collision analysis (merge, output both, output 1, etc?)
        for elem in chkCollision(ovlp1, ovlp2): #===
            conts3.append(elem)
    # add left over contours to merged list
    while len(conts1) != 0:
        conts3.append(conts1.pop())
    while len(conts2) != 0:
        conts3.append(conts2.pop())                              
    print( 'conts3:\n'+str([cont.name for cont in conts3]) )    
    return conts3

def boxOvlps(c1, c2): #=== being moved into contour class
    '''True if overlap between bounding boxes'''
    if c1._shape == None or c2._shape == None:
        print('INVALID SHAPE')
        quit() #=== dbug
        return False
    return c1.box().intersects( c2.box() ) or c1.box().touches( c2.box() )
def chkOvlp(c1,c2):
    '''Returns True if:
        (for closed contours): same name, bounding box overlaps and area of intersection > 0
        (for open contours): same name, same # pts and distance btwn them < threshold'''
    threshold = (1+2**(-17))
    # Closed traces
    if c1.closed and c2.closed and c1.name == c2.name:
        AoI = c1._shape.intersection( c2._shape ).area # area of intersection
        return boxOvlps(c1,c2) and AoI > 0 
    
    # Open traces
    elif not c1.closed and not c2.closed and c1.name == c2.name:
        if len(c1.points) != len(c2.points):
            return False
        # Lists of world coords to compare
        a = c1.transform.worldpts(c1.points)
        b = c2.transform.worldpts(c2.points)
        distlist = [distance(a[i],b[i]) for i in range(len(c1.points))] 
        for elem in distlist:
            if elem > threshold:
                return False
        return True
    return False

def distance(pt0, pt1):
    return math.sqrt( (pt0[0] - pt1[0])**2 + (pt0[1] - pt1[1])**2 )





main()


