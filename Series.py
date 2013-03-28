from ObjectList import *
from Contour import *
from ZContour import *
from xmlTree import *
class Series:
    '''<Series> is an object with attributes: name \
as well as a list containing all of the <Sections> objects associated with
it'''
# Python functions
    # INITIALIZE
    def __init__(self, xmlTree):
        '''Receives an xml file that is a list of sections in the form \
of an xml file. _list for <Sections>, _contours for <Contours>&<ZContours>'''
##        self._name = str(path_to_sections)
        self._tag = 'Series'
        self._list = ObjectList()
    # Variables extracted from file
        # Those that need to be in list type are done so below
        self._index = int(xmlTree._tree.getroot().attrib['index'])
        self._viewport = xmlTree._tree.getroot().attrib['viewport'] #str --modified--> list
        self._units = str(xmlTree._tree.getroot().attrib['units'])
        self._autoSaveSeries = bool(xmlTree._tree.getroot().attrib['autoSaveSeries'].capitalize())
        self._autoSaveSection = bool(xmlTree._tree.getroot().attrib['autoSaveSection'].capitalize())
        self._warnSaveSection = bool(xmlTree._tree.getroot().attrib['warnSaveSection'].capitalize())
        self._beepDeleting = bool(xmlTree._tree.getroot().attrib['beepDeleting'].capitalize())
        self._beepPaging = bool(xmlTree._tree.getroot().attrib['beepPaging'].capitalize())
        self._hideTraces = bool(xmlTree._tree.getroot().attrib['hideTraces'].capitalize())
        self._unhideTraces = bool(xmlTree._tree.getroot().attrib['unhideTraces'].capitalize())
        self._hideDomains = bool(xmlTree._tree.getroot().attrib['hideDomains'].capitalize())
        self._unhideDomains = bool(xmlTree._tree.getroot().attrib['unhideDomains'].capitalize())
        self._useAbsolutePaths = bool(xmlTree._tree.getroot().attrib['useAbsolutePaths'].capitalize())
        self._defaultThickness = float(xmlTree._tree.getroot().attrib['defaultThickness'])
        self._zMidSection = bool(xmlTree._tree.getroot().attrib['zMidSection'].capitalize())
        self._thumbWidth = int(xmlTree._tree.getroot().attrib['thumbWidth'])
        self._thumbHeight = int(xmlTree._tree.getroot().attrib['thumbHeight'])
        self._fitThumbSections = bool(xmlTree._tree.getroot().attrib['fitThumbSections'].capitalize())
        self._firstThumbSection = int(xmlTree._tree.getroot().attrib['firstThumbSection'])
        self._lastThumbSection = int(xmlTree._tree.getroot().attrib['lastThumbSection'])
        self._skipSections = int(xmlTree._tree.getroot().attrib['skipSections'])
        self._displayThumbContours = bool(xmlTree._tree.getroot().attrib['displayThumbContours'].capitalize())
        self._useFlipbookStyle = bool(xmlTree._tree.getroot().attrib['useFlipbookStyle'].capitalize())
        self._flipRate = int(xmlTree._tree.getroot().attrib['flipRate'])
        self._useProxies = bool(xmlTree._tree.getroot().attrib['useProxies'].capitalize())
        self._widthUseProxies = int(xmlTree._tree.getroot().attrib['widthUseProxies'])
        self._heightUseProxies = int(xmlTree._tree.getroot().attrib['heightUseProxies'])
        self._scaleProxies = float(xmlTree._tree.getroot().attrib['scaleProxies'])
        self._significantDigits = int(xmlTree._tree.getroot().attrib['significantDigits'])
        self._defaultBorder = xmlTree._tree.getroot().attrib['defaultBorder'] #str --modified--> list
        self._defaultFill = xmlTree._tree.getroot().attrib['defaultFill'] #str --modified--> list
        self._defaultMode = int(xmlTree._tree.getroot().attrib['defaultMode'])
        self._defaultName = str(xmlTree._tree.getroot().attrib['defaultName'])
        self._defaultComment = str(xmlTree._tree.getroot().attrib['defaultComment'])
        self._listSectionThickness = bool(xmlTree._tree.getroot().attrib['listSectionThickness'].capitalize())
        self._listDomainSource = bool(xmlTree._tree.getroot().attrib['listDomainSource'].capitalize())
        self._listDomainPixelsize = bool(xmlTree._tree.getroot().attrib['listDomainPixelsize'].capitalize())
        self._listDomainLength = bool(xmlTree._tree.getroot().attrib['listDomainLength'].capitalize())
        self._listDomainArea = bool(xmlTree._tree.getroot().attrib['listDomainArea'].capitalize())
        self._listDomainMidpoint = bool(xmlTree._tree.getroot().attrib['listDomainMidpoint'].capitalize())
        self._listTraceComment = bool(xmlTree._tree.getroot().attrib['listTraceComment'].capitalize())
        self._listTraceLength = bool(xmlTree._tree.getroot().attrib['listTraceLength'].capitalize())
        self._listTraceArea = bool(xmlTree._tree.getroot().attrib['listTraceArea'].capitalize())
        self._listTraceCentroid = bool(xmlTree._tree.getroot().attrib['listTraceCentroid'].capitalize())
        self._listTraceExtent = bool(xmlTree._tree.getroot().attrib['listTraceExtent'].capitalize())
        self._listTraceZ = bool(xmlTree._tree.getroot().attrib['listTraceZ'].capitalize())
        self._listTraceThickness = bool(xmlTree._tree.getroot().attrib['listTraceThickness'].capitalize())
        self._listObjectRange = bool(xmlTree._tree.getroot().attrib['listObjectRange'].capitalize())
        self._listObjectCount = bool(xmlTree._tree.getroot().attrib['listObjectCount'].capitalize())
        self._listObjectSurfarea = bool(xmlTree._tree.getroot().attrib['listObjectSurfarea'].capitalize())
        self._listObjectFlatarea = bool(xmlTree._tree.getroot().attrib['listObjectFlatarea'].capitalize())
        self._listObjectVolume = bool(xmlTree._tree.getroot().attrib['listObjectVolume'].capitalize())
        self._listZTraceNote = bool(xmlTree._tree.getroot().attrib['listZTraceNote'].capitalize())
        self._listZTraceRange = bool(xmlTree._tree.getroot().attrib['listZTraceRange'].capitalize())
        self._listZTraceLength = bool(xmlTree._tree.getroot().attrib['listZTraceLength'].capitalize())
        self._borderColors = xmlTree._tree.getroot().attrib['borderColors'] #str --modified--> list
        self._fillColors = xmlTree._tree.getroot().attrib['fillColors'] #str --modified--> list
        self._offset3D = xmlTree._tree.getroot().attrib['offset3D'] #str --modified--> list
        self._type3Dobject = int(xmlTree._tree.getroot().attrib['type3Dobject'])
        self._first3Dsection = int(xmlTree._tree.getroot().attrib['first3Dsection'])
        self._last3Dsection = int(xmlTree._tree.getroot().attrib['last3Dsection'])
        self._max3Dconnection = int(xmlTree._tree.getroot().attrib['max3Dconnection'])
        self._upper3Dfaces = bool(xmlTree._tree.getroot().attrib['upper3Dfaces'].capitalize())
        self._lower3Dfaces = bool(xmlTree._tree.getroot().attrib['lower3Dfaces'].capitalize())
        self._faceNormals = bool(xmlTree._tree.getroot().attrib['faceNormals'].capitalize())
        self._vertexNormals = bool(xmlTree._tree.getroot().attrib['vertexNormals'].capitalize())
        self._facets3D = int(xmlTree._tree.getroot().attrib['facets3D'])
        self._dim3D = xmlTree._tree.getroot().attrib['dim3D'] #str --modified--> list
        self._gridType = int(xmlTree._tree.getroot().attrib['gridType'])
        self._gridSize = xmlTree._tree.getroot().attrib['gridSize'] #str --modified--> list
        self._gridDistance = xmlTree._tree.getroot().attrib['gridDistance'] #str --modified--> list
        self._gridNumber = xmlTree._tree.getroot().attrib['gridNumber'] #str --modified--> list
        self._hueStopWhen = int(xmlTree._tree.getroot().attrib['hueStopWhen'])
        self._hueStopValue = int(xmlTree._tree.getroot().attrib['hueStopValue'])
        self._satStopWhen = int(xmlTree._tree.getroot().attrib['satStopWhen'])
        self._satStopValue = int(xmlTree._tree.getroot().attrib['satStopValue'])
        self._brightStopWhen = int(xmlTree._tree.getroot().attrib['brightStopWhen'])
        self._brightStopValue = int(xmlTree._tree.getroot().attrib['brightStopValue'])
        self._tracesStopWhen = bool(xmlTree._tree.getroot().attrib['tracesStopWhen'].capitalize())
        self._areaStopPercent = int(xmlTree._tree.getroot().attrib['areaStopPercent'])
        self._areaStopSize = int(xmlTree._tree.getroot().attrib['areaStopSize'])
        self._ContourMaskWidth = int(xmlTree._tree.getroot().attrib['ContourMaskWidth'])
        self._smoothingLength = int(xmlTree._tree.getroot().attrib['smoothingLength'])
        self._mvmtIncrement = xmlTree._tree.getroot().attrib['mvmtIncrement'] #str --modified--> list
        self._ctrlIncrement = xmlTree._tree.getroot().attrib['ctrlIncrement'] #str --modified--> list
        self._shiftIncrement = xmlTree._tree.getroot().attrib['shiftIncrement'] #str --modified--> list
        self._contours = ObjectList() #List of <Contour> and <ZContour> objects
        ######### Variable modifications ================
        #self._contours
        for node in xmlTree.gettreelist():
            if node.tag == 'Contour':
                C = Contour(node)
                self._contours.addO(C)
            elif node.tag == 'ZContour': #=========
                Z = ZContour(node)
                self._contours.addO(Z)
        # viewport
        rawList = list(self._viewport.split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        self._viewport = tmpList
        #defaultBorder
        rawList = list(self._defaultBorder.split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        self._defaultBorder = tmpList
        #defaultFill
        rawList = list(self._defaultFill.split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        self._defaultFill = tmpList
        #borderColors (Floating points are reduced to 0.0 if no other digits)
        #May need to output as 0.000 later =====================
            #Split up string into a list of strings containing 3 float points 
        splitList = self._borderColors.replace(',','').split('   ')
            #Make a list of lists containing floating points
        refinedList = []
        for elem in splitList:
            if elem != '':
                strfloats = elem.split(' ')
                intfloats = []
                #Turn strings into floats
                for num in strfloats:
                    num = float(num)
                    intfloats.append(num)
                refinedList.append(intfloats)
        self._borderColors = refinedList  
        #fillColors (Floating points are reduced to 0.0 if no other digits)
        #May need to output as 0.000 later =====================
            #Split up string into a list of strings containing 3 float points 
        splitList = self._fillColors.replace(',','').split('   ')
            #Make a list of lists containing floating points
        refinedList = []
        for elem in splitList:
            if elem != '':
                strfloats = elem.split(' ')
                intfloats = []
                #Turn strings into floats
                for num in strfloats:
                    num = float(num)
                    intfloats.append(num)
                refinedList.append(intfloats)
        self._fillColors = refinedList
        #offset3D
        rawList = list(self._offset3D.split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        self._offset3D = tmpList
        #dim3D
        rawList = list(self._dim3D.split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        self._dim3D = tmpList
        #gridSize
        rawList = list(self._gridSize.split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        self._gridSize = tmpList
        #gridDistance
        rawList = list(self._gridDistance.split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        self._gridDistance = tmpList
        #gridNumber
        rawList = list(self._gridNumber.split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        self._gridNumber = tmpList
        #mvmtIncrement
        rawList = list(self._mvmtIncrement.split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        self._mvmtIncrement = tmpList
        #ctrlIncrement
        rawList = list(self._ctrlIncrement.split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        self._ctrlIncrement = tmpList
        #shiftIncrement
        rawList = list(self._shiftIncrement.split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        self._shiftIncrement = tmpList
        
        
    # INDEX REPRESENTATION
    def __getitem__(self,x):
        '''Allows use of <Section>[x] to return xth elements in list'''
        return self._list[x]
    # STRING REPRESENTATION
    def __str__(self):
        '''Allows use of print(<Series>) function.'''
        return 'Name: %s\nTag: %s' %(self.getname(),self.gettag())

# Accessors
    def getname(self):
        return self._name
    def gettag(self):
        return self._tag
    def printsections(self):
        '''Prints the name of all the sections in a series'''
        for elem in self._list._list:
            print(elem._name)

# Mutators
    def chgname(self, x):
        self._name = str(x)
    def chgtag(self, x):
        self._tag = str(x)
    def addsection(self, section):
        '''Adds a <Section> object to <Series> object'''
        self._list._list.append(section)