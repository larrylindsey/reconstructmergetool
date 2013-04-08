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
        self._tag = 'Series'
        self._name = xmlTree._name
        self._list = []
        self._attribs = ['index', 'viewport', 'units', 'autoSaveSeries', \
        'autoSaveSection', 'warnSaveSection', 'beepDeleting', 'beepPaging', \
        'hideTraces', 'unhideTraces', 'hideDomains', 'unhideDomains', 'useAbsolutePaths', \
        'defaultThickness', 'zMidSection', 'thumbWidth', 'thumbHeight', 'fitThumbSections', \
        'firstThumbSection', 'lastThumbSection', 'skipSections', 'displayThumbContours', \
        'useFlipbookStyle', 'flipRate', 'useProxies', 'widthUseProxies', 'heightUseProxies', \
        'scaleProxies', 'significantDigits', 'defaultBorder', 'defaultFill', 'defaultMode', \
        'defaultName', 'defaultComment', 'listSectionThickness', 'listDomainSource', \
        'listDomainPixelsize', 'listDomainLength', 'listDomainArea', 'listDomainMidpoint', \
        'listTraceComment', 'listTraceLength', 'listTraceArea', 'listTraceCentroid', \
        'listTraceExtent', 'listTraceZ', 'listTraceThickness', 'listObjectRange', \
        'listObjectCount', 'listObjectSurfarea', 'listObjectFlatarea', 'listObjectVolume', \
        'listZTraceNote', 'listZTraceRange', 'listZTraceLength', 'borderColors', 'fillColors', \
        'offset3D', 'type3Dobject', 'first3Dsection', 'last3Dsection', 'max3Dconnection', \
        'upper3Dfaces', 'lower3Dfaces', 'faceNormals', 'vertexNormals', 'facets3D', 'dim3D', \
        'gridType', 'gridSize', 'gridDistance', 'gridNumber', 'hueStopWhen', 'hueStopValue', \
        'satStopWhen', 'satStopValue', 'brightStopWhen', 'brightStopValue', 'tracesStopWhen', \
        'areaStopPercent', 'areaStopSize', 'ContourMaskWidth', 'smoothingLength', \
        'mvmtIncrement', 'ctrlIncrement', 'shiftIncrement']
        self._index = int(xmlTree._tree.getroot().attrib['index'])
        self._viewport = self.popviewport(xmlTree)
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
        self._defaultBorder = self.popdefborder(xmlTree)
        self._defaultFill = self.popdeffill(xmlTree)
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
        self._borderColors = self.popbordcolors(xmlTree)
        self._fillColors = self.popfillcolors(xmlTree)
        self._offset3D = self.popoffset3D(xmlTree)
        self._type3Dobject = int(xmlTree._tree.getroot().attrib['type3Dobject'])
        self._first3Dsection = int(xmlTree._tree.getroot().attrib['first3Dsection'])
        self._last3Dsection = int(xmlTree._tree.getroot().attrib['last3Dsection'])
        self._max3Dconnection = int(xmlTree._tree.getroot().attrib['max3Dconnection'])
        self._upper3Dfaces = bool(xmlTree._tree.getroot().attrib['upper3Dfaces'].capitalize())
        self._lower3Dfaces = bool(xmlTree._tree.getroot().attrib['lower3Dfaces'].capitalize())
        self._faceNormals = bool(xmlTree._tree.getroot().attrib['faceNormals'].capitalize())
        self._vertexNormals = bool(xmlTree._tree.getroot().attrib['vertexNormals'].capitalize())
        self._facets3D = int(xmlTree._tree.getroot().attrib['facets3D'])
        self._dim3D = self.popdim3D(xmlTree)
        self._gridType = int(xmlTree._tree.getroot().attrib['gridType'])
        self._gridSize = self.popgridsize(xmlTree)
        self._gridDistance = self.popgriddistance(xmlTree)
        self._gridNumber = self.popgridnumber(xmlTree)
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
        self._mvmtIncrement = self.popmvmtincrement(xmlTree)
        self._ctrlIncrement = self.popctrlincrement(xmlTree)
        self._shiftIncrement = self.popshiftincrement(xmlTree)
        self._contours = self.popcontours(xmlTree)   
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
    def getattribs(self):
        '''Attributes as strings for XML OUTPUT FORMATTING'''
        return (self._index, self._viewport, self._units, self._autoSaveSeries, \
        self._autoSaveSection, self._warnSaveSection, self._beepDeleting, self._beepPaging, \
        self._hideTraces, self._unhideTraces, self._hideDomains, self._unhideDomains, self._useAbsolutePaths, \
        self._defaultThickness, self._zMidSection, self._thumbWidth, self._thumbHeight, self._fitThumbSections, \
        self._firstThumbSection, self._lastThumbSection, self._skipSections, self._displayThumbContours, \
        self._useFlipbookStyle, self._flipRate, self._useProxies, self._widthUseProxies, self._heightUseProxies, \
        self._scaleProxies, self._significantDigits, self._defaultBorder, self._defaultFill, self._defaultMode, \
        self._defaultName, self._defaultComment, self._listSectionThickness, self._listDomainSource, \
        self._listDomainPixelsize, self._listDomainLength, self._listDomainArea, self._listDomainMidpoint, \
        self._listTraceComment, self._listTraceLength, self._listTraceArea, self._listTraceCentroid, \
        self._listTraceExtent, self._listTraceZ, self._listTraceThickness, self._listObjectRange, \
        self._listObjectCount, self._listObjectSurfarea, self._listObjectFlatarea, self._listObjectVolume, \
        self._listZTraceNote, self._listZTraceRange, self._listZTraceLength, self._borderColors, self._fillColors, \
        self._offset3D, self._type3Dobject, self._first3Dsection, self._last3Dsection, self._max3Dconnection, \
        self._upper3Dfaces, self._lower3Dfaces, self._faceNormals, self._vertexNormals, self._facets3D, self._dim3D, \
        self._gridType, self._gridSize, self._gridDistance, self._gridNumber, self._hueStopWhen, self._hueStopValue, \
        self._satStopWhen, self._satStopValue, self._brightStopWhen, self._brightStopValue, self._tracesStopWhen, \
        self._areaStopPercent, self._areaStopSize, self._ContourMaskWidth, self._smoothingLength, \
        self._mvmtIncrement, self._ctrlIncrement, self._shiftIncrement)
        

# Mutators
    def chgname(self, x):
        self._name = str(x)
    def chgtag(self, x):
        self._tag = str(x)
    def addsection(self, section):
        '''Adds a <Section> object to <Series> object'''
        self._list.append(section)
    def popcontours(self, xmlTree):
        #self._contours
        ret = []
        for node in xmlTree.gettreelist():
            if node.tag == 'Contour':
                C = Contour(node)
                ret.append(C)
            elif node.tag == 'ZContour': #=========
                Z = ZContour(node)
                ret.append(Z)
        return ret
    def popviewport(self, xmlTree):
        # viewport
        rawList = list(xmlTree._tree.getroot().attrib['viewport'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popdefborder(self, xmlTree):
        #defaultBorder
        rawList = list(xmlTree._tree.getroot().attrib['defaultBorder'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popdeffill(self, xmlTree):
        #defaultFill
        rawList = list(xmlTree._tree.getroot().attrib['defaultFill'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popbordcolors(self, xmlTree):
        #borderColors (Floating points are reduced to 0.0 if no other digits)
        #May need to output as 0.000 later =====================
            #Split up string into a list of strings containing 3 float points 
        splitList = xmlTree._tree.getroot().attrib['borderColors'].replace(',','').split('   ')
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
        return refinedList
    def popfillcolors(self, xmlTree): 
        #fillColors (Floating points are reduced to 0.0 if no other digits)
        #May need to output as 0.000 later =====================
            #Split up string into a list of strings containing 3 float points 
        splitList = xmlTree._tree.getroot().attrib['fillColors'].replace(',','').split('   ')
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
        return refinedList
    def popoffset3D(self, xmlTree):
        #offset3D
        rawList = list(xmlTree._tree.getroot().attrib['offset3D'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popdim3D(self, xmlTree):
        #dim3D
        rawList = list(xmlTree._tree.getroot().attrib['dim3D'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popgridsize(self, xmlTree):
        #gridSize
        rawList = list(xmlTree._tree.getroot().attrib['gridSize'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popgriddistance(self, xmlTree):
        #gridDistance
        rawList = list(xmlTree._tree.getroot().attrib['gridDistance'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popgridnumber(self, xmlTree):
        #gridNumber
        rawList = list(xmlTree._tree.getroot().attrib['gridNumber'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popmvmtincrement(self, xmlTree):
        #mvmtIncrement
        rawList = list(xmlTree._tree.getroot().attrib['mvmtIncrement'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popctrlincrement(self, xmlTree):
        #ctrlIncrement
        rawList = list(xmlTree._tree.getroot().attrib['ctrlIncrement'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popshiftincrement(self, xmlTree):
        #shiftIncrement
        rawList = list(xmlTree._tree.getroot().attrib['shiftIncrement'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList