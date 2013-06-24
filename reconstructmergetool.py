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
#  Date Last Modified: 6/24/2013
#
# Currently working on:
        # Make list of conflicts
        # Series contours in mergeSerAtts
        # sections sorted in computer way(? lol) (i.e. 12 after 111)
        # GUI: PySide
        # tospace() fromspace() in transform

        
'''Merge two series together'''
import sys, os, re
from Series import *
from lxml import etree as ET
import PyQt4

if len(sys.argv) > 1:
    ser = os.path.basename(sys.argv[1]) # Name of series
    ser2 = os.path.basename(sys.argv[2]) 
    inpath = os.path.abspath(os.path.dirname(sys.argv[1]))+'/' # Directory of series
    inpath2 = os.path.abspath(os.path.dirname(sys.argv[2]))+'/'
    mergeoutpath = os.path.dirname(os.path.dirname(inpath))+'/merged/' #===

def main():
    if __name__ != '__main__':
        print('Welcome to reconstructmergetool')
        return
    if len(sys.argv) > 1:
        #1)Create series object
        series = getSeriesXML( inpath+ser )
        series2 = getSeriesXML( inpath2+ser2 )
        #2)Append sections to series
        series.getSectionsXML( inpath+ser )
        series2.getSectionsXML( inpath2+ser2 )
        #3)Merge series
        series3 = mergeSeries( series, series2 )
        #4)Output series file
        series3.writeseries( mergeoutpath )
        #5)Output section file(s)
        series3.writesections( mergeoutpath )
        
def getSeriesXML(path_to_series, name=None):
    '''Creates a series object representation from a .ser XML file in path_to_series'''
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

# Series stuff
def mergeSeries(serObj1, serObj2, name=None):
    '''Takes in two series objects and returns a 3rd, merged series object'''
    if name == None: # If not specified...
        name = serObj1.name #... output series will have same name as serObj1
        
    # Make series object and merge attributes
    serObj3 = mergeSerAtts(serObj1, serObj2, name)
    # Merge series contours===
    serObj3.contours = mergeSerConts(serObj1, serObj2) 
    
    # Create list of parallel section pairs (paired by section name)
    pairlist = [(x,y) for x in serObj1.sections for y in serObj2.sections if x.name.partition('.')[2] == y.name.partition('.')[2]  ]
    
    # Merge sections
    print('Merging Sections...')
    for (x,y) in pairlist:
        print(x.name+' '+y.name)
        serObj3.sections.append( mergeSections(x,y,name) )
    print('...DONE')
    return serObj3
def mergeSerAtts(ser1Obj, ser2Obj, ser3name):
    print('Merging Series Attributes...'),
    # Compare and merge series attributes from ser1Obj/ser2Obj
    ser1atts = ser1Obj.output()[0] # Dictionary of attributes
    ser2atts = ser2Obj.output()[0] # "
    ser3atts = {}
    for att in ser1atts:
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
    print('DONE')
    return ser3conts



# Section stuff
def mergeSections(sec1, sec2, ser3name):
    '''compares and merges the attributes associated with Sections (except contours).
    i.e. imgs, index, thickness, alignLocked'''
    # Populate shapely polygons
    for contour in sec1.contours:
        contour.popshape()
    for contour in sec2.contours:
        contour.popshape()    
    # create section for merge
    sec3 = mergeSecAtts(sec1, sec2, chkSecAtts(sec1,sec2))
    # check section images
    sec3.imgs = chkSecImgs(sec1,sec2)
    # chkContOvlps
    sec3.contours = mergeSecConts(sec1, sec2)
    return sec3
def chkSecAtts(sec1, sec2):
    '''Returns dictionary of True/False for each attribute, describing if they are the same between both sections'''
    chkDict = {}
    # chk attributes
    s1atts = sec1.output()
    s2atts = sec2.output()
    for att in s1atts:
        chkDict[att] = (s1atts[att] == s2atts[att])
    return chkDict
def mergeSecAtts(sec1, sec2, chkDict):
    '''Takes in two sections and a chkDict from chkSecAtts, returns merged section attributes (non-Contour/images)'''
    s1atts = sec1.output()
    s2atts = sec2.output()
    s3atts = {}
    for att in chkDict:
        if not chkDict[att]:
            a = raw_input('CONFLICT: mergeSecAtts')
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
    # Do they have the same number of images?
    if len(s1.imgs) != len(s2.imgs):
        return mergeSecImgs(s1,s2)
    # Do the images contain the same data?
    for i in range( len(s1.imgs) ):
        if s1.imgs[i].output() != s2.imgs[i].output():
            return mergeSecImgs(s1,s2)
    # If all the same, just copy 1st series' images
    return s1.imgs
def mergeSecImgs(s1,s2): #=== currently copies s1.imgs
    return s1.imgs
def mergeSecConts(s1,s2):
    '''Returns merged contours between two sections'''
    # Lists of all contours in parallel sections
    conts1 = [cont for cont in s1.contours]
    conts2 = [cont for cont in s2.contours] 
    conts3 = []
    while len(conts1) != 0 and len(conts2) != 0:
        for elem in mergeOvlpConts( *retOvlpConts(conts1, conts2) ): # * expands tuple
            conts3.append( elem )
    # Append leftover, non-overlapping contours
    while len(conts1) != 0:
        conts3.append( conts1.pop() )
    while len(conts2) != 0:
        conts3.append( conts2.pop() )
    return conts3

def retOvlpConts(conts1, conts2):
    '''Returns lists of mutually overlapping contours'''
    ovlp1 = [conts1.pop()]
    ovlp2 = []
    # Check sec2 for conts that ovlp with ovlp1
    for cont in conts2:
        if ovlp1[0].overlaps(cont) != 0 and ovlp1[0].name == cont.name:
            ovlp2.append(cont)
            conts2.remove(cont)
    # Now find overlaps in s1 that ovlp with ovlp2 conts
    for cont in ovlp2:
        for cont2 in conts1:
            if cont.overlaps(cont2) != 0 and cont.name == cont2.name:
                ovlp1.append(cont2)
                conts1.remove(cont2)
    return ovlp1, ovlp2
def mergeOvlpConts(ovlp1, ovlp2):
    '''Handles lists of overlapping contours, returns list of handled contours'''
    output = []
    if len(ovlp2) == 0:
        output.append(ovlp1.pop())
    else:
        for elem in ovlp1:
            for elem2 in ovlp2:
                if elem.overlaps(elem2) == 1: # If contours are the same -> merge and output
                    output.append(elem)
                else: # If contours overlap, but not 100% -> user input
                    a = raw_input('CONFLICT NEEDS RESOLVING '+elem.name+' '+elem2.name)
                    if a == 1:
                        output.append(elem)
                    elif a == 2:
                        output.append(elem2)
                    else:
                        output.append(elem)
                        output.append(elem2)
    return output

main()


