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
        self._defaultBorder = self.popdefborder(root) #===
        self._defaultFill = self.popdeffill(root) #===
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
        self._borderColors = self.popbordcolors(root) #===
        self._fillColors = self.popfillcolors(root) #===
        self._offset3D = self.popoffset3D(root) #===
        self._type3Dobject = int(root.attrib['type3Dobject'])
        self._first3Dsection = int(root.attrib['first3Dsection'])
        self._last3Dsection = int(root.attrib['last3Dsection'])
        self._max3Dconnection = int(root.attrib['max3Dconnection'])
        self._upper3Dfaces = bool(root.attrib['upper3Dfaces'].capitalize())
        self._lower3Dfaces = bool(root.attrib['lower3Dfaces'].capitalize())
        self._faceNormals = bool(root.attrib['faceNormals'].capitalize())
        self._vertexNormals = bool(root.attrib['vertexNormals'].capitalize())
        self._facets3D = int(root.attrib['facets3D'])
        self._dim3D = self.popdim3D(root) #===
        self._gridType = int(root.attrib['gridType'])
        self._gridSize = self.popgridsize(root) #===
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
        self._ctrlIncrement = self.popctrlincrement(root) #===
        self._shiftIncrement = self.popshiftincrement(root) #===
    # INDEX REPRESENTATION
    def __getitem__(self,x):
        '''Allows use of <Section>[x] to return xth elements in list'''
        return self._list[x]
    # STRING REPRESENTATION
    def __str__(self):
        '''Allows use of print(<Series>) function.'''
        return 'Name: %s\nTag: %s' %(self.getname(),self.gettag())

# Accessors
    def output(self): #==
        '''Returns a dictionary of attributes and a list of contours for building .ser xml file'''
        attributes = {}
        keys = self._attribs
        values = list(self.xgetattribs())
        count = 0
        for value in values:
            attributes[keys[count]] = value
            count += 1
        return attributes, self._contours
    def getattribs(self):
        '''Returns attributes as appropriate python data type'''
    def xgetattribs(self):
        '''Returns attributes in appropriate format for xml output'''
        return (str(self._index), str(self.getviewport()), str(self._units), str(self._autoSaveSeries).lower(), \
        str(self._autoSaveSection).lower(), str(self._warnSaveSection).lower(), str(self._beepDeleting).lower(), str(self._beepPaging).lower(), \
        str(self._hideTraces).lower(), str(self._unhideTraces).lower(), str(self._hideDomains).lower(), str(self._unhideDomains).lower(), str(self._useAbsolutePaths).lower(), \
        str(self._defaultThickness), str(self._zMidSection).lower(), str(self._thumbWidth), str(self._thumbHeight), str(self._fitThumbSections).lower(), \
        str(self._firstThumbSection), str(self._lastThumbSection), str(self._skipSections), str(self._displayThumbContours).lower(), \
        str(self._useFlipbookStyle).lower(), str(self._flipRate), str(self._useProxies).lower(), str(self._widthUseProxies), str(self._heightUseProxies), \
        str(self._scaleProxies), str(self._significantDigits), str(self._defaultBorder), str(self._defaultFill), str(self._defaultMode), \
        str(self._defaultName), str(self._defaultComment), str(self._listSectionThickness).lower(), str(self._listDomainSource).lower(), \
        str(self._listDomainPixelsize).lower(), str(self._listDomainLength).lower(), str(self._listDomainArea).lower(), str(self._listDomainMidpoint).lower(), \
        str(self._listTraceComment).lower(), str(self._listTraceLength).lower(), str(self._listTraceArea).lower(), str(self._listTraceCentroid), \
        str(self._listTraceExtent).lower(), str(self._listTraceZ).lower(), str(self._listTraceThickness).lower(), str(self._listObjectRange).lower(), \
        str(self._listObjectCount).lower(), str(self._listObjectSurfarea).lower(), str(self._listObjectFlatarea).lower(), str(self._listObjectVolume).lower(), \
        str(self._listZTraceNote).lower(), str(self._listZTraceRange).lower(), str(self._listZTraceLength).lower(), str(self._borderColors), str(self._fillColors), \
        str(self._offset3D), str(self._type3Dobject), str(self._first3Dsection), str(self._last3Dsection), str(self._max3Dconnection), \
        str(self._upper3Dfaces).lower(), str(self._lower3Dfaces).lower(), str(self._faceNormals).lower(), str(self._vertexNormals).lower(), str(self._facets3D), str(self._dim3D), \
        str(self._gridType), str(self._gridSize), str(self._gridDistance), str(self._gridNumber), str(self._hueStopWhen), str(self._hueStopValue), \
        str(self._satStopWhen), str(self._satStopValue), str(self._brightStopWhen), str(self._brightStopValue), str(self._tracesStopWhen).lower(), \
        str(self._areaStopPercent), str(self._areaStopSize), str(self._ContourMaskWidth), str(self._smoothingLength), \
        str(self._mvmtIncrement), str(self._ctrlIncrement), str(self._shiftIncrement))
    def getviewport(self):
        ret = ''
        for float in self._viewport:
            ret += str(float)+' '
        return ret.rstrip()

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
    def popbordcolors(self, root): #=== should be new line every 3 pts in xml
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
    def popfillcolors(self, root): #=== should be new line every 3 pts in xml
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