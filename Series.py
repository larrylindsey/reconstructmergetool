from Contour import *
from ZContour import *
class Series:
    '''<Series> is an object with attributes: name \
as well as a list containing all of the <Sections> objects associated with
it'''
# Python functions
    # INITIALIZE
    def __init__(self, root, name='Unknown'):
        '''Receives an xml file that is a list of sections in the form \
of an xml file. _list for <Sections>, _contours for <Contours>&<ZContours>'''
        self._name = name
        self._tag = root.tag
        self._contours = self.popcontours(root)
        self._sections = []
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
        self._index = int(root.attrib['index'])
        self._viewport = self.popviewport(root)
        self._units = str(root.attrib['units'])
        self._autoSaveSeries = bool(root.attrib['autoSaveSeries'].capitalize())
        self._autoSaveSection = bool(root.attrib['autoSaveSection'].capitalize())
        self._warnSaveSection = bool(root.attrib['warnSaveSection'].capitalize())
        self._beepDeleting = bool(root.attrib['beepDeleting'].capitalize())
        self._beepPaging = bool(root.attrib['beepPaging'].capitalize())
        self._hideTraces = bool(root.attrib['hideTraces'].capitalize())
        self._unhideTraces = bool(root.attrib['unhideTraces'].capitalize())
        self._hideDomains = bool(root.attrib['hideDomains'].capitalize())
        self._unhideDomains = bool(root.attrib['unhideDomains'].capitalize())
        self._useAbsolutePaths = bool(root.attrib['useAbsolutePaths'].capitalize())
        self._defaultThickness = float(root.attrib['defaultThickness'])
        self._zMidSection = bool(root.attrib['zMidSection'].capitalize())
        self._thumbWidth = int(root.attrib['thumbWidth'])
        self._thumbHeight = int(root.attrib['thumbHeight'])
        self._fitThumbSections = bool(root.attrib['fitThumbSections'].capitalize())
        self._firstThumbSection = int(root.attrib['firstThumbSection'])
        self._lastThumbSection = int(root.attrib['lastThumbSection'])
        self._skipSections = int(root.attrib['skipSections'])
        self._displayThumbContours = bool(root.attrib['displayThumbContours'].capitalize())
        self._useFlipbookStyle = bool(root.attrib['useFlipbookStyle'].capitalize())
        self._flipRate = int(root.attrib['flipRate'])
        self._useProxies = bool(root.attrib['useProxies'].capitalize())
        self._widthUseProxies = int(root.attrib['widthUseProxies'])
        self._heightUseProxies = int(root.attrib['heightUseProxies'])
        self._scaleProxies = float(root.attrib['scaleProxies'])
        self._significantDigits = int(root.attrib['significantDigits'])
        self._defaultBorder = self.popdefborder(root)
        self._defaultFill = self.popdeffill(root)
        self._defaultMode = int(root.attrib['defaultMode'])
        self._defaultName = str(root.attrib['defaultName'])
        self._defaultComment = str(root.attrib['defaultComment'])
        self._listSectionThickness = bool(root.attrib['listSectionThickness'].capitalize())
        self._listDomainSource = bool(root.attrib['listDomainSource'].capitalize())
        self._listDomainPixelsize = bool(root.attrib['listDomainPixelsize'].capitalize())
        self._listDomainLength = bool(root.attrib['listDomainLength'].capitalize())
        self._listDomainArea = bool(root.attrib['listDomainArea'].capitalize())
        self._listDomainMidpoint = bool(root.attrib['listDomainMidpoint'].capitalize())
        self._listTraceComment = bool(root.attrib['listTraceComment'].capitalize())
        self._listTraceLength = bool(root.attrib['listTraceLength'].capitalize())
        self._listTraceArea = bool(root.attrib['listTraceArea'].capitalize())
        self._listTraceCentroid = bool(root.attrib['listTraceCentroid'].capitalize())
        self._listTraceExtent = bool(root.attrib['listTraceExtent'].capitalize())
        self._listTraceZ = bool(root.attrib['listTraceZ'].capitalize())
        self._listTraceThickness = bool(root.attrib['listTraceThickness'].capitalize())
        self._listObjectRange = bool(root.attrib['listObjectRange'].capitalize())
        self._listObjectCount = bool(root.attrib['listObjectCount'].capitalize())
        self._listObjectSurfarea = bool(root.attrib['listObjectSurfarea'].capitalize())
        self._listObjectFlatarea = bool(root.attrib['listObjectFlatarea'].capitalize())
        self._listObjectVolume = bool(root.attrib['listObjectVolume'].capitalize())
        self._listZTraceNote = bool(root.attrib['listZTraceNote'].capitalize())
        self._listZTraceRange = bool(root.attrib['listZTraceRange'].capitalize())
        self._listZTraceLength = bool(root.attrib['listZTraceLength'].capitalize())
        self._borderColors = self.popbordcolors(root)
        self._fillColors = self.popfillcolors(root)
        self._offset3D = self.popoffset3D(root)
        self._type3Dobject = int(root.attrib['type3Dobject'])
        self._first3Dsection = int(root.attrib['first3Dsection'])
        self._last3Dsection = int(root.attrib['last3Dsection'])
        self._max3Dconnection = int(root.attrib['max3Dconnection'])
        self._upper3Dfaces = bool(root.attrib['upper3Dfaces'].capitalize())
        self._lower3Dfaces = bool(root.attrib['lower3Dfaces'].capitalize())
        self._faceNormals = bool(root.attrib['faceNormals'].capitalize())
        self._vertexNormals = bool(root.attrib['vertexNormals'].capitalize())
        self._facets3D = int(root.attrib['facets3D'])
        self._dim3D = self.popdim3D(root)
        self._gridType = int(root.attrib['gridType'])
        self._gridSize = self.popgridsize(root)
        self._gridDistance = self.popgriddistance(root)
        self._gridNumber = self.popgridnumber(root)
        self._hueStopWhen = int(root.attrib['hueStopWhen'])
        self._hueStopValue = int(root.attrib['hueStopValue'])
        self._satStopWhen = int(root.attrib['satStopWhen'])
        self._satStopValue = int(root.attrib['satStopValue'])
        self._brightStopWhen = int(root.attrib['brightStopWhen'])
        self._brightStopValue = int(root.attrib['brightStopValue'])
        self._tracesStopWhen = bool(root.attrib['tracesStopWhen'].capitalize())
        self._areaStopPercent = int(root.attrib['areaStopPercent'])
        self._areaStopSize = int(root.attrib['areaStopSize'])
        self._ContourMaskWidth = int(root.attrib['ContourMaskWidth'])
        self._smoothingLength = int(root.attrib['smoothingLength'])
        self._mvmtIncrement = self.popmvmtincrement(root)
        self._ctrlIncrement = self.popctrlincrement(root)
        self._shiftIncrement = self.popshiftincrement(root)  
    # INDEX REPRESENTATION
    def __getitem__(self,x):
        '''Allows use of <Section>[x] to return xth elements in list'''
        return self._list[x]
    # STRING REPRESENTATION
    def __str__(self):
        '''Allows use of print(<Series>) function.'''
        return 'Name: %s\nTag: %s' %(self.getname(),self.gettag())

# Accessors
    def output(self, outpath): #==
        '''Creates a series (.ser) file in outpath'''
        attributes = {}
        keys = self._attribs
        values = list(self.getattribs())
        count = 0
        for value in values:
            attributes[keys[count]] = value
            count += 1
        return attributes
    
    
    def getname(self):
        return self._name
    def gettag(self):
        return self._tag
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
        self._sections.append(section)
    def popcontours(self, root):
        #self._contours
        ret = []
        for child in root:
            if child.tag == 'Contour':
                C = Contour(child)
                ret.append(C)
            elif child.tag == 'ZContour': #=========
                Z = ZContour(child)
                ret.append(Z)
        return ret
    def popviewport(self, root):
        # viewport
        rawList = list(root.attrib['viewport'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popdefborder(self, root):
        #defaultBorder
        rawList = list(root.attrib['defaultBorder'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popdeffill(self, root):
        #defaultFill
        rawList = list(root.attrib['defaultFill'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popbordcolors(self, root):
        #borderColors (Floating points are reduced to 0.0 if no other digits)
        #May need to output as 0.000 later =====================
            #Split up string into a list of strings containing 3 float points 
        splitList = root.attrib['borderColors'].replace(',','').split('   ')
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
    def popfillcolors(self, root): 
        #fillColors (Floating points are reduced to 0.0 if no other digits)
        #May need to output as 0.000 later =====================
            #Split up string into a list of strings containing 3 float points 
        splitList = root.attrib['fillColors'].replace(',','').split('   ')
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
    def popoffset3D(self, root):
        #offset3D
        rawList = list(root.attrib['offset3D'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popdim3D(self, root):
        #dim3D
        rawList = list(root.attrib['dim3D'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popgridsize(self, root):
        #gridSize
        rawList = list(root.attrib['gridSize'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popgriddistance(self, root):
        #gridDistance
        rawList = list(root.attrib['gridDistance'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popgridnumber(self, root):
        #gridNumber
        rawList = list(root.attrib['gridNumber'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popmvmtincrement(self, root):
        #mvmtIncrement
        rawList = list(root.attrib['mvmtIncrement'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popctrlincrement(self, root):
        #ctrlIncrement
        rawList = list(root.attrib['ctrlIncrement'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popshiftincrement(self, root):
        #shiftIncrement
        rawList = list(root.attrib['shiftIncrement'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList