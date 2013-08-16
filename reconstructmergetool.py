#! /usr/bin/env python
#  Files: reconstructmergetool.py, rmtgui.py, Series.py, Section.py, Transform.py,
#         Contour.py, ZContour.py, Image.py, mergeObject.py, reScale.py, findCalFactor.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite, Larry Lindsey
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 8/16/2013
#
# To do:
    # Needs to be a better way to change image contour and section.img stuff simultaneously
        # check for multiple images is in beta (Section.py)
    # verbosity mode
    # make series object better, dictionary instead of a bunch of attributes?
    # tospace() fromspace() in transform

        
'''Merge two series together'''
import sys, os
from Series import *
from Section import *
from Transform import *
from Image import *
from Contour import *
from ZContour import *
from lxml import etree as ET
import time
from skimage import transform as tf

if len(sys.argv) >= 3:
    ser = os.path.basename( sys.argv[1] ) # Name of series
    ser2 = os.path.basename( sys.argv[2] ) 
    inpath = os.path.abspath( os.path.dirname(sys.argv[1]) )+'/' # Directory of series
    inpath2 = os.path.abspath( os.path.dirname(sys.argv[2]) )+'/'
    if len(sys.argv) == 4:
        mergeoutpath = os.path.abspath(sys.argv[3])+'/merged/' #===
    else:
        mergeoutpath = os.path.dirname( os.path.dirname(inpath) )+'/merged/' #===

def main():
    if __name__ != '__main__':
        print('Welcome to reconstructmergetool')
        return
    if len(sys.argv) > 1:
        #1)Create series object
        series = getSeries( inpath+ser )
        series2 = getSeries( inpath2+ser2 )
        
        #2)Merge series attributes
        mergeSer = mergeSeries( series, series2 )
        mergeSer.sections = mergeAllSections( series, series2 )

        #4)Output .ser file
        mergeSer.writeseries( mergeoutpath )
        
        #5)Output section file(s)
        mergeSer.writesections( mergeoutpath )

def getSeries(path_to_series):
    '''Create a series object, fully populated.'''
    if path_to_series.find(os.sep) < 0:
        path_to_series = './' + path_to_series
    series = getSeriesXML(path_to_series)
    series.getSectionsXML(path_to_series)
    return series
    
def getSeriesXML(path_to_series):
    '''Creates a series object representation from a .ser XML file in path_to_series'''
    print('Creating series object from ' + path_to_series + '...'),
    #Parse series
    tree = ET.parse( path_to_series )
    
    root = tree.getroot() #Series
    #Create series object
    series = Series(root, path_to_series.split('/')[len(path_to_series.split('/'))-1].replace('.ser',''))
    print('DONE')
    print('\tSeries: '+series.name)
    return series

def serAttHandler(ser1atts, ser2atts, ser3atts, conflicts):
    '''Resolves conflicts regarding series attributes'''
    for conflict in conflicts:
        print('\nSeries attributes do not match: '+str(conflict))
        print('1: '+ser1atts[conflict]+'\n'+'2: '+ser2atts[conflict])
        a = 3
        while a not in [1,2]:
            a = int(raw_input('Choose attribute to pass to output series... 1 or 2: '))
            if a == 1:
                ser3atts[conflict] = ser1atts[conflict]
            elif a == 2:
                ser3atts[conflict] = ser2atts[conflict]
            else:
                print('Invalid choice. Please enter 1 or 2')
    return ser3atts
    
def serContHandler(ser1conts, ser2conts, ser3conts):
    # add leftover, unique zcontours to ser3conts
    ser3conts.extend(ser1conts)
    ser3conts.extend(ser2conts)
    while len(ser3conts) > 20:
        print('Current length: '+str(len(ser3conts)))
        a = raw_input('Too many series contours to output, enter index of contour to delete\n'\
                      +str([cont.name for cont in ser3conts]))
        ser3conts.pop( int(a) )
        print('\n')
    return ser3conts
def serZContHandler(ser1zconts, ser2zconts, ser3zconts ):
    # add leftover, unique zcontours to ser3zconts
    ser3zconts.extend(ser1zconts)
    ser3zconts.extend(ser2zconts)
    return ser3zconts
def secAttHandler(s1atts, s2atts, comparison):
    mergedAttributes = {}
    for att in comparison:
        if not comparison[att]:
            a = raw_input('CONFLICT: mergeSecAtts')
            if a == 1:
                mergedAttributes[att] = s1atts[att]
            else:
                mergedAttributes[att] = s2atts[att]
        else:
            mergedAttributes[att] = s1atts[att]
    return mergedAttributes

def secImgHandler(s1,s2):
    s3imgs = []
    print('1: '+str(s1.imgs[0].output()))
    print('2: '+str(s2.imgs[0].output()))
    a='hello'
    while str(a) not in ['1','2']:
        a = raw_input('Enter image to use in merged series: ')
        if str(a).lower() == '1':
            s3imgs = s1.imgs
        elif str(a).lower() == '2':
            s3imgs = s2.imgs
    return s3imgs

def secContHandler(ovlp1, ovlp2):
    '''Handles lists of overlapping contours, returns list of handled contours. Checks for 100% ovlp first'''
    output = []
    if len(ovlp2) == 0:
        output.append(ovlp1.pop())

    # Check for same contours and remove (prevents unnecessary user input)
    for elem in ovlp1:
        for elem2 in ovlp2:
            if elem.overlaps(elem2) == 1: # If contours are the same -> merge and output
                output.append( elem )
                ovlp1.remove( elem )
                ovlp2.remove( elem2 )
                
    # Check rest of contours
    for elem in ovlp1:
        for elem2 in ovlp2:
            if elem.overlaps(elem2) != 1 and elem.overlaps(elem2) != 0: # If contours overlap, but not 100% -> user input
                print('Contour overlap conflict:\n'+'1:\n'+str(elem)+'\n'+'2\n: '+str(elem2))
                print( 'AoU/AoI: '+str(elem.overlaps(elem2)) )
                a = raw_input('Choose which contour to output (3 to output both): ')
                if a == 1:
                    output.append( elem )
                    ovlp1.remove( elem )
                    ovlp2.remove( elem2 )
                elif a == 2:
                    output.append( elem2 )
                    ovlp1.remove( elem )
                    ovlp2.remove( elem2 )
                else:
                    output.append( elem )
                    output.append( elem2 )
                    ovlp1.remove( elem )
                    ovlp2.remove( elem2 )
    return output

def mergeSeries(serObj1, serObj2, name=None, \
                mergeSerAttfxn = serAttHandler, \
                mergeSerContfxn = serContHandler, \
                mergeSerZContfxn = serZContHandler):
    '''Returns a merged series object as defined by the mergefxn parameters. The <Series>.sections will \
    be empty and must be populated with a mergeSections function'''
    
    print('Merging series objects...'),
    if not name:
        name = serObj1.name
    
    # Create merged parts    
    mergedAtts = mergeSeriesAttributes( serObj1, serObj2, handler=mergeSerAttfxn)
    mergedConts = mergeSeriesContours( serObj1.contours, serObj2.contours, handler=mergeSerContfxn)
    mergedZConts = mergeSeriesZContours( serObj1.contours, serObj2.contours, handler=mergeSerZContfxn)
    mergedSeries = Series( root=ET.Element('Series',mergedAtts), name=name ) # Create series w/ merged atts
    mergedSeries.contours = list(mergedConts+mergedZConts) # Append merged Contours/ZContours
    print('DONE')
    
    return mergedSeries

def mergeSeriesAttributes(serObj1, serObj2, handler=serAttHandler ):
    '''Merges the attributes from two series. Conflicts handled with handler parameter.
    Attributes are returned in the form of a dictionary.'''
    # Compare and merge series attributes from ser1Obj/ser2Obj
    # Handle conflict independently
    ser1atts = serObj1.output()[0]
    ser2atts = serObj2.output()[0]
    ser3atts = {}
    conflicts = {}
    for att in ser1atts:
        # If the same -> merge to ser3atts...
        if ser1atts[att] == ser2atts[att]:
            ser3atts[att] = ser1atts[att]
        # ...otherwise, add to conflicts dictionary
        else:
            conflicts[att] = True
    return handler(ser1atts, ser2atts, ser3atts, conflicts)

def mergeSeriesContours(ser1conts, ser2conts, handler=serContHandler):
    '''Merges the contours from two series. Conflicts handled with handler parameter.
    Contours returned in the form of a list.'''
    ser1conts = [cont for cont in ser1conts if cont.tag == 'Contour']
    ser2conts = [cont for cont in ser2conts if cont.tag == 'Contour']
    ser3conts = []
    for elem in ser1conts:
        for elem2 in ser2conts:
            if elem == elem2: # Merge same contours
                ser3conts.append( elem )
                ser1conts.remove( elem )
                ser2conts.remove( elem2 )
    return handler(ser1conts, ser2conts, ser3conts)
    
def mergeSeriesZContours(ser1conts, ser2conts, handler=serZContHandler):
    ser1zconts = [cont for cont in ser1conts if cont.tag == 'ZContour']
    ser2zconts = [cont for cont in ser2conts if cont.tag == 'ZContour']
    ser3zconts = []
    for elem in ser1zconts:
        for elem2 in ser2zconts:
            if elem.name == elem2.name and elem.overlaps(elem2):
                ser3zconts.append( elem ) 
                ser1zconts.remove( elem )
                ser2zconts.remove( elem2 )
    return handler(ser1zconts, ser2zconts, ser3zconts)

def mergeAllSections(serObj1, serObj2, name=None, \
                     secAttfxn = secAttHandler, \
                     secImgfxn = secImgHandler, \
                     secContfxn = secContHandler, \
                     attOverride = None, \
                     imageOverride = None, \
                     contOverride = None):
    '''Takes in two series, returns list of merged sections'''
    print('Merging Sections...')
    # Create list of parallel section pairs (paired by section name)
    pairlist = [(x,y) for x in serObj1.sections for y in serObj2.sections if x.index == y.index]
     
    # Merge sections
    mergedSections = []
    for (x,y) in pairlist:
        print(x.name+' '+y.name)
        mergedSections.append( mergeSection(x,y, name, \
                                            secAttfxn = secAttfxn, \
                                            secImgfxn = secImgfxn, \
                                            secContfxn = secContfxn, \
                                            attOverride = attOverride, \
                                            imageOverride = imageOverride, \
                                            contOverride = contOverride) )
    print('...DONE')
    return mergedSections

def mergeSection(sec1, sec2, name=None, \
                 secAttfxn = secAttHandler, \
                 secImgfxn = secImgHandler, \
                 secContfxn = secContHandler, \
                 attOverride = None, \
                 imageOverride = None, \
                 contOverride = None):
    '''Takes in two sections, returns a 3rd merged section'''
    # Populate shapely polygons
    for contour in sec1.contours: contour.popshape()
    for contour in sec2.contours: contour.popshape()    
    # create section w/ merged attributes
    if attOverride != None:
        if int(attOverride) == 1:
            sec3 = mergeSectionAttributes(sec1, sec1, name, handler=secAttfxn)
        elif int(attOverride) == 2:
            sec3 = mergeSectionAttributes(sec2, sec2, name, handler=secAttfxn)
    else:
        sec3 = mergeSectionAttributes( sec1, sec2, name, handler=secAttfxn )
    # check section images
    if imageOverride != None:
        if int(imageOverride) == 1:
            sec3.imgs = sec1.imgs
        elif int(imageOverride) == 2:
            sec3.imgs = sec2.imgs
        elif int(imageOverride) == 3:
            sec3.imgs = (sec1.imgs).extend(sec2.imgs)
    else:
        sec3.imgs = mergeSectionImgs( sec1, sec2, handler=secImgfxn )
    # merge section contours
    if contOverride != None:
        if int(contOverride) == 1:
            sec3.contours = sec1.contours
        elif int(contOverride) == 2:
            sec3.contours = sec2.contours
        elif int(contOverride) == 3:
            sec3.contours = (sec1.contours).extend(sec2.contours)
    else:
        sec3.contours = mergeSectionContours( sec1, sec2, handler=secContfxn )
    return sec3

def checkSectionAttributes(sec1, sec2):
    '''Returns dictionary of True/False for each attribute,
    describing if they are the same between both sections'''
    chkDict = {}
    # chk attributes
    s1atts = sec1.output()
    s2atts = sec2.output()
    for att in s1atts:
        chkDict[att] = (s1atts[att] == s2atts[att])
    return chkDict

def mergeSectionAttributes(sec1, sec2, name=None, handler=secAttHandler):
    '''Takes in two sections and a chkDict from chkSecAtts,
    returns merged section attributes (non-Contour/images)'''
    comparisonDict = checkSectionAttributes(sec1, sec2)
    mergedAttributes = handler( sec1.output(), sec2.output(), comparisonDict )
    
    # Create element tree Section element
    elem = ET.Element('Section')
    for att in mergedAttributes:
        elem.set(str(att), mergedAttributes[att])
    if not name: #=== sec1 name?
        name = sec1.name
    else:
        name = name+'.'+str(sec1.index)
    sec3 = Section(elem, name)
    return sec3

def mergeSectionImgs(s1, s2, handler=secImgHandler):
    '''Returns imgs to be addeded to new section'''
    # Do they have the same number of images?
    if len(s1.imgs) != len(s2.imgs):
        return handler(s1,s2)
    # Do the images contain the same data?
    for i in range( len(s1.imgs) ):
        if not s1.imgs[i] == s2.imgs[i]:
            return handler(s1,s2)
    # If all the same, just copy 1st series' images
    return s1.imgs

def checkOverlappingConts(conts1, conts2):
    '''Returns lists of mutually overlapping contours'''
    ovlp1 = [conts1.pop()]
    ovlp2 = []
    # Check sec2 for conts that ovlp with ovlp1
    for cont in conts2:
        if ovlp1[0].name == cont.name and ovlp1[0].overlaps(cont) != 0:
            ovlp2.append(cont)
            conts2.remove(cont)
    # Now find overlaps in s1 that ovlp with ovlp2 conts
    for cont in ovlp2:
        for cont2 in conts1:
            if cont.name == cont2.name and cont.overlaps(cont2) != 0:
                ovlp1.append(cont2)
                conts1.remove(cont2)
    return ovlp1, ovlp2

def mergeSectionContours(s1,s2, handler=secContHandler):
    '''Returns merged contours between two sections'''
    # Lists of all contours in parallel sections
    conts1 = [cont for cont in s1.contours]
    conts2 = [cont for cont in s2.contours]
    conts3 = []
    while len(conts1) != 0 and len(conts2) != 0:
        for elem in handler( *checkOverlappingConts(conts1,conts2) ):
            conts3.append( elem )
    # Append leftover, non-overlapping contours
    conts3.extend(conts1)
    conts3.extend(conts2)
    return conts3

def bethBellMerge(): #===
    # First load FPNCT_BB and delete everything except those in saveList
    saveList = [re.compile('[d][0-9]{0,2}vftz[0-9]{0,2}[a-z]?$', re.I),
                re.compile('[d][0-9]{0,2}vftzcfa[0-9]{0,2}[a-z]?$', re.I),
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}[a-z]?$', re.I),
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}dcv[0-9]{0,2}[a-z]?$', re.I),
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}dssvdh[0-9]{0,2}[a-z]?$', re.I),
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}dssvrh[0-0]{0,2}[a-z]?$', re.I),
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}dssvrhclose[0-9]{0,2}[a-z]?$', re.I),
                re.compile('[d][0-9]{0,2}c[0-9]{0,2}[a-z]?$', re.I),
                re.compile('[d][0-9]{0,2}c[0-9]{0,2}scale[0-9]{0,2}[a-z]?$', re.I),
                re.compile('[d][0-9]{0,2}cfa[0-9]{0,2}[a-z]?$', re.I)]
    ser1 = getSeries('/home/michaelm/Documents/Test Series/bb/FPNCT_BB/FPNCT.ser')
    for section in ser1.sections:
        savedContours = []
        for contour in section.contours:
            for prog in saveList:
                if len(prog.findall(contour.name)) != 0:
                    savedContours.append(contour)
                    break
        section.contours = savedContours
    
    # Now load FPNCT_JNB and delete everything in delList
    delList = [re.compile('[d][0-9]{0,2}c[0-9]{0,2}[a-z]?$', re.I),
               re.compile('[d][0-9]{0,2}cfa[0-9]{0,2}[a-z]?$', re.I)]
    
    ser2 = getSeries('/home/michaelm/Documents/Test Series/bb/FPNCT_JNB/FPNCT.ser')
    for section in ser2.sections:
        deletedContours = []
        for contour in section.contours:
            for prog in delList:
                if len(prog.findall(contour.name)) != 0:
                    deletedContours.append(contour.name)
                    break
        section.contours = [cont for cont in section.contours if cont.name not in deletedContours]
    
    ser3 = mergeSeries(ser1, ser2, name='FPNCT_merge')
    # imageOverride set to 2; imageOverride 1 has different image and domain1 transforms
    ser3.sections = mergeAllSections(ser1, ser2, name='FPNCT_merge', imageOverride=2)
    ser3.writeseries('/home/michaelm/Documents/Test Series/bb/FPNCT_merge/')
    ser3.writesections('/home/michaelm/Documents/Test Series/bb/FPNCT_merge/')
    
class mergeObject:
    '''Abstract class to easily change functions for reconstructmergetool.py'''
    def __init__(self):
        
        # META STUFF
        self.name = 'newSeries'
        self.outputPath = os.getcwd()+'/'+str(self.name)+'/'
        
        # SERIES MERGE FUNCTIONS
        self.handleSerAtts = serAttHandler
        self.handleSerConts = serContHandler
        self.handleSerZConts = serZContHandler
        
        # SECTION MERGE FUNCTIONS
        self.handleSecAtts = secAttHandler
        self.handleSecImgs = secImgHandler
        self.handleSecConts = secContHandler

# Fxns
    def merge(self, path_to_series1, path_to_series2):
        '''Merges two series together based on mergeObjects' attributes'''
        s1 = getSeries(path_to_series1)
        s2 = getSeries(path_to_series2)

        mergedSeries = mergeSeries( s1, s2, name = self.name, \
                                mergeSerAttfxn = self.handleSerAtts, \
                                mergeSerContfxn = self.handleSerConts, \
                                mergeSerZContfxn = self.handleSerZConts  )
        
        mergedSeries.sections = mergeAllSections( s1, s2, self.name, \
                                              secAttfxn = self.handleSecAtts, \
                                              secImgfxn = self.handleSecImgs, \
                                              secContfxn = self.handleSecConts)
        mergedSeries.writeseries( self.outputPath )
        mergedSeries.writesections( self.outputPath )
        
# Setters
    def setName(self, string):
        self.name = str(string)
        self.outputPath = os.getcwd()+'/'+str(self.name)+'/'
        print('Merged series name changed to: '+self.name)
        print
        
    def setOutpath(self, string):
        self.outputPath = str(string)
        print('New output path set: '+self.outputPath)
        print
        
    def setSerAttfxn(self, fxn):
        self.handleSerAtts = fxn
        print('New series attribute handler set')
        print
        
    def setSerContfxn(self, fxn):
        self.handleSerConts = fxn
        print('New series contour handler set')
        
    def setSerZContfxn(self, fxn):
        self.handleSerZConts = fxn
        print('New series zcontour handler set')
        
    def setSecAttfxn(self, fxn):
        self.handleSecAtts = fxn
        print('New section attribute handler set')
        print
        
    def setSecImgfxn(self, fxn):
        self.handleSecImgs = fxn
        print('New section image handler set')
        print
        
    def setSecContfxn(self, fxn):
        self.handleSecConts = fxn
        print('New section contour handler set')
        print
    def current(self):
        print('CURRENT MERGEOBJECT SETTINGS:')
        print('Name: '+str(self.name))
        print('Outpath: '+str(self.outputPath))
        print
        print('Series Attribute Handler: '+str(self.handleSerAtts))
        print('Series Contour Handler: '+str(self.handleSerConts))
        print('Series ZContour Handler: '+str(self.handleSerZConts))
        print
        print('Section Attribute Handler: '+str(self.handleSecAtts))
        print('Section Image Handler: '+str(self.handleSecImgs))
        print('Section Contour Handler: '+str(self.handleSecConts))
main()

