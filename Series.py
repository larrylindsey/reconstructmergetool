from Contour import *
from ZContour import *
# Recent changes: popgridSize int -> float
class Series:
    '''<Series> is an object with attributes: name \
as well as a list containing all of the <Sections> objects associated with
it'''
# Python functions
    # INITIALIZE
    def __init__(self, root=None, name='No Name'):
        '''Receives an xml file (root) that is a list of sections in the form \
of an xml file. self.sections for <Sections>, self.contours for <Contours>&<ZContours>'''
        self.name = name
        self.tag = self.poptag(root)
        self.contours = self.popcontours(root)
        self.sections = [] #Sorted in reconstructmergetool.py, getsections()
        self.index = self.popindex(root)
        self.viewport = self.popviewport(root)
        self.units = self.popunits(root)
        self.autoSaveSeries = self.popautoSaveSeries
        self.autoSaveSection =  self.s2b(self.popautoSaveSection(root))
        self.warnSaveSection = self.s2b(self.popwarnSaveSection(root))
        self.beepDeleting = self.s2b(self.popbeepDeleting(root))
        self.beepPaging = self.s2b(self.popbeepPaging(root))
        self.hideTraces = self.s2b(self.pophideTraces(root))
        self.unhideTraces = self.s2b(self.popunhideTraces(root))
        self.hideDomains = self.s2b(self.pophideDomains(root))
        self.unhideDomains = self.s2b(self.popunhideDomains(root))
        self.useAbsolutePaths = self.s2b(self.popuseAbsolutePaths(root))
        self.defaultThickness = self.popdefaultThickness(root) #float
        self.zMidSection = self.s2b(self.popzMidSection(root))
        self.thumbWidth = self.popthumbWidth(root) #int
        self.thumbHeight = self.popthumbHeight(root) #int
        self.fitThumbSections = self.s2b(self.popfitThumbSections(root))
        self.firstThumbSection = self.popfirstThumbSection(root) #int
        self.lastThumbSection = self.poplastThumbSection(root) #int
        self.skipSections = self.popskipSections(root) #int
        self.displayThumbContours = self.s2b(self.popdisplayThumbContours(root))
        self.useFlipbookStyle = self.s2b(self.popuseFlipbookStyle(root))
        self.flipRate = self.popflipRate(root) #int
        self.useProxies = self.s2b(self.popuseProxies(root))
        self.widthUseProxies = self.popwidthUseProxies(root) #int
        self.heightUseProxies = self.popheightUseProxies(root) #int
        self.scaleProxies = self.popscaleProxies(root) #float
        self.significantDigits = self.popsignificantDigits(root) #int
        self.defaultBorder = self.popdefborder(root)
        self.defaultFill = self.popdeffill(root)
        self.defaultMode = self.popdefaultMode(root) #int
        self.defaultName = self.popdefaultName(root)
        self.defaultComment = self.popdefaultComment(root)
        self.listSectionThickness = self.s2b(self.poplistSectionThickness(root))
        self.listDomainSource = self.s2b(self.poplistDomainSource(root))
        self.listDomainPixelsize = self.s2b(self.poplistDomainPixelsize(root))
        self.listDomainLength = self.s2b(self.poplistDomainLength(root))
        self.listDomainArea = self.s2b(self.poplistDomainArea(root))
        self.listDomainMidpoint = self.s2b(self.poplistDomainMidpoint(root))
        self.listTraceComment = self.s2b(self.poplistTraceComment(root))
        self.listTraceLength = self.s2b(self.poplistTraceLength(root))
        self.listTraceArea = self.s2b(self.poplistTraceArea(root))
        self.listTraceCentroid = self.s2b(self.poplistTraceCentroid(root))
        self.listTraceExtent = self.s2b(self.poplistTraceExtent(root))
        self.listTraceZ = self.s2b(self.poplistTraceZ(root))
        self.listTraceThickness = self.s2b(self.poplistTraceThickness(root))
        self.listObjectRange = self.s2b(self.poplistObjectRange(root))
        self.listObjectCount = self.s2b(self.poplistObjectCount(root))
        self.listObjectSurfarea = self.s2b(self.poplistObjectSurfarea(root))
        self.listObjectFlatarea = self.s2b(self.poplistObjectFlatarea(root))
        self.listObjectVolume = self.s2b(self.poplistObjectVolume(root))
        self.listZTraceNote = self.s2b(self.poplistZTraceNote(root))
        self.listZTraceRange = self.s2b(self.poplistZTraceRange(root))
        self.listZTraceLength = self.s2b(self.poplistZTraceLength(root))
        self.borderColors = self.popbordcolors(root)
        self.fillColors = self.popfillcolors(root)
        self.offset3D = self.popoffset3D(root)
        self.type3Dobject = self.poptype3Dobject(root) #int
        self.first3Dsection = self.popfirst3Dsection(root) #int
        self.last3Dsection = self.poplast3Dsection(root) #int
        self.max3Dconnection = self.popmax3Dconnection(root) #int
        self.upper3Dfaces = self.s2b(self.popupper3Dfaces(root))
        self.lower3Dfaces = self.s2b(self.poplower3Dfaces(root))
        self.faceNormals = self.s2b(self.popfaceNormals(root))
        self.vertexNormals = self.s2b(self.popvertexNormals(root))
        self.facets3D = self.popfacets3D(root) #int
        self.dim3D = self.popdim3D(root)
        self.gridType = self.popgridType(root) #int
        self.gridSize = self.popgridsize(root)
        self.gridDistance = self.popgriddistance(root)
        self.gridNumber = self.popgridnumber(root)
        self.hueStopWhen = self.pophueStopWhen(root) #int
        self.hueStopValue = self.pophueStopValue(root) #int
        self.satStopWhen = self.popsatStopWhen(root) #int
        self.satStopValue = self.popsatStopValue(root) #int
        self.brightStopWhen = self.popbrightStopWhen(root) #int
        self.brightStopValue = self.popbrightStopValue(root) #int
        self.tracesStopWhen = self.s2b(self.poptracesStopWhen(root))
        self.areaStopPercent = self.popareaStopPercent(root) #int
        self.areaStopSize = self.popareaStopSize(root) #int
        self.ContourMaskWidth = self.popContourMaskWidth(root) #int
        self.smoothingLength = self.popsmoothingLength(root) #int
        self.mvmtIncrement = self.popmvmtincrement(root)
        self.ctrlIncrement = self.popctrlincrement(root)
        self.shiftIncrement = self.popshiftincrement(root)
        # Private
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
        'mvmtIncrement', 'ctrlIncrement', 'shiftIncrement'] # List of all attributes, used for creating an attribute dictionary for output (see output(self))
    # Allows indexing of section object
    def __getitem__(self,x):
        '''Allows use of <Section>[x] to return xth elements in list'''
        return self._list[x]
    # print(<Section>) output
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
        return attributes, self.contours
    def xgetattribs(self):
        '''Returns attributes in appropriate format for xml output'''
        return (str(self.index), str(self.getviewport()), str(self.units), str(self.autoSaveSeries).lower(), \
        str(self.autoSaveSection).lower(), str(self.warnSaveSection).lower(), str(self.beepDeleting).lower(), str(self.beepPaging).lower(), \
        str(self.hideTraces).lower(), str(self.unhideTraces).lower(), str(self.hideDomains).lower(), str(self.unhideDomains).lower(), str(self.useAbsolutePaths).lower(), \
        str(self.defaultThickness), str(self.zMidSection).lower(), str(self.thumbWidth), str(self.thumbHeight), str(self.fitThumbSections).lower(), \
        str(self.firstThumbSection), str(self.lastThumbSection), str(self.skipSections), str(self.displayThumbContours).lower(), \
        str(self.useFlipbookStyle).lower(), str(self.flipRate), str(self.useProxies).lower(), str(self.widthUseProxies), str(self.heightUseProxies), \
        str(self.scaleProxies), str(self.significantDigits), str(self.getdefaultborder()), str(self.getdefaultfill()), str(self.defaultMode), \
        str(self.defaultName), str(self.defaultComment), str(self.listSectionThickness).lower(), str(self.listDomainSource).lower(), \
        str(self.listDomainPixelsize).lower(), str(self.listDomainLength).lower(), str(self.listDomainArea).lower(), str(self.listDomainMidpoint).lower(), \
        str(self.listTraceComment).lower(), str(self.listTraceLength).lower(), str(self.listTraceArea).lower(), str(self.listTraceCentroid).lower(), \
        str(self.listTraceExtent).lower(), str(self.listTraceZ).lower(), str(self.listTraceThickness).lower(), str(self.listObjectRange).lower(), \
        str(self.listObjectCount).lower(), str(self.listObjectSurfarea).lower(), str(self.listObjectFlatarea).lower(), str(self.listObjectVolume).lower(), \
        str(self.listZTraceNote).lower(), str(self.listZTraceRange).lower(), str(self.listZTraceLength).lower(), str(self.getbordercolors()), str(self.getfillcolors()), \
        str(self.getoffset3d()), str(self.type3Dobject), str(self.first3Dsection), str(self.last3Dsection), str(self.max3Dconnection), \
        str(self.upper3Dfaces).lower(), str(self.lower3Dfaces).lower(), str(self.faceNormals).lower(), str(self.vertexNormals).lower(), str(self.facets3D), str(self.getdim3d()), \
        str(self.gridType), str(self.getgridsize()), str(self.getgriddistance()), str(self.getgridnumber()), str(self.hueStopWhen), str(self.hueStopValue), \
        str(self.satStopWhen), str(self.satStopValue), str(self.brightStopWhen), str(self.brightStopValue), str(self.tracesStopWhen).lower(), \
        str(self.areaStopPercent), str(self.areaStopSize), str(self.ContourMaskWidth), str(self.smoothingLength), \
        str(self.getmvmntinc()), str(self.getctrlinc()), str(self.getshiftinc()))
    def getviewport(self):
        ret = ''
        for float in self.viewport:
            ret += str(float)+' '
        return ret.rstrip()
    def getdim3d(self):
        ret = ''
        for float in self.dim3D:
            ret += str(float)+' '
        return ret.rstrip()
    def getoffset3d(self):
        ret = ''
        for float in self.offset3D:
            ret += str(float)+' '
        return ret.rstrip()
    def getmvmntinc(self):
        ret = ''
        for float in self.mvmtIncrement:
            ret += str(float)+' '
        return ret.rstrip()
    def getctrlinc(self):
        ret = ''
        for float in self.ctrlIncrement:
            ret += str(float)+' '
        return ret.rstrip()
    def getshiftinc(self):
        ret = ''
        for float in self.shiftIncrement:
            ret += str(float)+' '
        return ret.rstrip()
    def getdefaultborder(self):
        ret = ''
        for float in self.defaultBorder:
            ret += str(float)+' '
        return ret.rstrip()
    def getdefaultfill(self):
        ret = ''
        for float in self.defaultFill:
            ret += str(float)+' '
        return ret.rstrip()
    def getgridsize(self):
        ret = ''
        for float in self.gridSize:
            ret += str(float)+' '
        return ret.rstrip()
    def getgriddistance(self):
        ret = ''
        for float in self.gridDistance:
            ret += str(float)+' '
        return ret.rstrip()
    def getgridnumber(self):
        ret = ''
        for float in self.gridNumber:
            ret += str(float)+' '
        return ret.rstrip()
    def getbordercolors(self):
        ret = ''
        for elem in self.borderColors: #elem is a list of 3 floats
            tmp = ''
            for flt in elem:
                tmp += str(flt)+' '
            ret += tmp.rstrip()+', '
        return ret.rstrip()
    def getfillcolors(self):
        ret = ''
        for elem in self.fillColors: #elem is a list of 3 floats
            tmp = ''
            for flt in elem:
                tmp += str(flt)+' '
            ret += tmp.rstrip()+', '   
        return ret.rstrip()

# Helper functions
    def s2b(self, string):
        '''Converts string to bool'''
        if str(string) == 'None':
            return None
        else:
            return string.lower() in ('true')
    def addsection(self, section):
        '''Adds a <Section> object to <Series> object'''
        self.sections.append(section)
    def popindex(self, root):
        if root == None:
            return None
        return int(root.attrib['index'])
    def popunits(self, root):
        if root == None:
            return None
        return str(root.attrib['units'])
    def poptag(self, root):
        if root == None:
            return None
        else:
            return root.tag
    def popcontours(self, root):
        #self.contours
        if root == None:
            return None
        ret = []
        for child in root:
            if child.tag == 'Contour':
                C = Contour(child)
                ret.append(C)
            elif child.tag == 'ZContour':
                Z = ZContour(child)
                ret.append(Z)
        return ret
    def popviewport(self, root):
        # viewport
        if root == None:
            return None
        rawList = list(root.attrib['viewport'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popdefborder(self, root):
        #defaultBorder
        if root == None:
            return None
        rawList = list(root.attrib['defaultBorder'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popdeffill(self, root):
        #defaultFill
        if root == None:
            return None
        rawList = list(root.attrib['defaultFill'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popbordcolors(self, root): #===
        if root == None:
            return None
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
        if root == None:
            return None
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
        if root == None:
            return None
        #offset3D
        rawList = list(root.attrib['offset3D'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popdim3D(self, root):
        if root == None:
            return None
        #dim3D
        rawList = list(root.attrib['dim3D'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popgridsize(self, root):
        if root == None:
            return None
        #gridSize
        rawList = list(root.attrib['gridSize'].split(' '))
        tmpList = []
        for elem in rawList: #===
            tmpList.append( float(elem) )
        return tmpList
    def popgriddistance(self, root):
        if root == None:
            return None
        #gridDistance
        rawList = list(root.attrib['gridDistance'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( int(elem) )
        return tmpList
    def popgridnumber(self, root):
        if root == None:
            return None
        #gridNumber
        rawList = list(root.attrib['gridNumber'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( int(elem) )
        return tmpList
    def popmvmtincrement(self, root):
        if root == None:
            return None
        #mvmtIncrement
        rawList = list(root.attrib['mvmtIncrement'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popctrlincrement(self, root):
        if root == None:
            return None
        #ctrlIncrement
        rawList = list(root.attrib['ctrlIncrement'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popshiftincrement(self, root):
        if root == None:
            return None
        #shiftIncrement
        rawList = list(root.attrib['shiftIncrement'].split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popautoSaveSeries(self, root):
        if root == None:
            return None
        return root.attrib['autoSaveSeries']
    def popautoSaveSection(self, root):
        if root == None:
            return None
        return root.attrib['autoSaveSection']
    def popwarnSaveSection(self, root):
        if root == None:
            return None
        return root.attrib['warnSaveSection']
    def popbeepDeleting(self, root):
        if root == None:
            return None
        return root.attrib['beepDeleting']
    def popbeepPaging(self, root):
        if root == None:
            return None
        return root.attrib['beepPaging']
    def pophideTraces(self, root):
        if root == None:
            return None
        return root.attrib['hideTraces']
    def popunhideTraces(self, root):
        if root == None:
            return None
        return root.attrib['unhideTraces']
    def pophideDomains(self, root):
        if root == None:
            return None
        return root.attrib['hideDomains']
    def popunhideDomains(self, root):
        if root == None:
            return None
        return root.attrib['unhideDomains']
    def popuseAbsolutePaths(self, root):
        if root == None:
            return None
        return root.attrib['useAbsolutePaths']
    def popdefaultThickness(self, root):
        if root == None:
            return None
        return root.attrib['defaultThickness']
    def popzMidSection(self, root):
        if root == None:
            return None
        return root.attrib['zMidSection']
    def popthumbWidth(self, root):
        if root == None:
            return None
        return float(root.attrib['thumbWidth'])
    def popthumbHeight(self, root):
        if root == None:
            return None
        return int(root.attrib['thumbHeight'])
    def popfitThumbSections(self, root):
        if root == None:
            return None
        return root.attrib['fitThumbSections']
    def popfirstThumbSection(self, root):
        if root == None:
            return None
        return int(root.attrib['firstThumbSection'])
    def poplastThumbSection(self, root):
        if root == None:
            return None
        return int(root.attrib['lastThumbSection'])
    def popskipSections(self, root):
        if root == None:
            return None
        return int(root.attrib['skipSections'])
    def popdisplayThumbContours(self, root):
        if root == None:
            return None
        return root.attrib['displayThumbContours']
    def popuseFlipbookStyle(self, root):
        if root == None:
            return None
        return root.attrib['useFlipbookStyle']
    def popflipRate(self, root):
        if root == None:
            return None
        return int(root.attrib['flipRate'])
    def popuseProxies(self, root):
        if root == None:
            return None
        return root.attrib['useProxies']
    def popwidthUseProxies(self, root):
        if root == None:
            return None
        return root.attrib['widthUseProxies']
    def popheightUseProxies(self, root):
        if root == None:
            return None
        return int(root.attrib['heightUseProxies'])
    def popscaleProxies(self, root):
        if root == None:
            return None
        return float(root.attrib['scaleProxies'])
    def popsignificantDigits(self, root):
        if root == None:
            return None
        return int(root.attrib['significantDigits'])
    def popdefaultMode(self, root):
        if root == None:
            return None
        return int(root.attrib['defaultMode'])
    def popdefaultName(self, root):
        if root == None:
            return None
        return root.attrib['defaultName']
    def popdefaultComment(self, root):
        if root == None:
            return None
        return root.attrib['defaultComment']
    def poplistSectionThickness(self, root):
        if root == None:
            return None
        return root.attrib['listSectionThickness']
    def poplistDomainSource(self, root):
        if root == None:
            return None
        return root.attrib['listDomainSource']
    def poplistDomainPixelsize(self, root):
        if root == None:
            return None
        return root.attrib['listDomainPixelsize']
    def poplistDomainLength(self, root):
        if root == None:
            return None
        return root.attrib['listDomainLength']
    def poplistDomainArea(self, root):
        if root == None:
            return None
        return root.attrib['listDomainArea']
    def poplistDomainMidpoint(self, root):
        if root == None:
            return None
        return root.attrib['listDomainMidpoint']
    def poplistTraceComment(self, root):
        if root == None:
            return None
        return root.attrib['listTraceComment']
    def poplistTraceLength(self, root):
        if root == None:
            return None
        return root.attrib['listTraceLength']
    def poplistTraceArea(self, root):
        if root == None:
            return None
        return root.attrib['listTraceArea']
    def poplistTraceCentroid(self, root):
        if root == None:
            return None
        return root.attrib['listTraceCentroid']
    def poplistTraceExtent(self, root):
        if root == None:
            return None
        return root.attrib['listTraceExtent']
    def poplistTraceZ(self, root):
        if root == None:
            return None
        return root.attrib['listTraceZ']
    def poplistTraceThickness(self, root):
        if root == None:
            return None
        return root.attrib['listTraceThickness']
    def poplistObjectRange(self, root):
        if root == None:
            return None
        return root.attrib['listObjectRange']
    def poplistObjectCount(self, root):
        if root == None:
            return None
        return root.attrib['listObjectCount']
    def poplistObjectSurfarea(self, root):
        if root == None:
            return None
        return root.attrib['listObjectSurfarea']
    def poplistObjectFlatarea(self, root):
        if root == None:
            return None
        return root.attrib['listObjectFlatarea']
    def poplistObjectVolume(self, root):
        if root == None:
            return None
        return root.attrib['listObjectVolume']
    def poplistZTraceNote(self, root):
        if root == None:
            return None
        return root.attrib['listZTraceNote']
    def poplistZTraceRange(self, root):
        if root == None:
            return None
        return root.attrib['listZTraceRange']
    def poplistZTraceLength(self, root):
        if root == None:
            return None
        return root.attrib['listZTraceLength']
    def poptype3Dobject(self, root):
        if root == None:
            return None
        return int(root.attrib['type3Dobject'])
    def popfirst3Dsection(self, root):
        if root == None:
            return None
        return int(root.attrib['first3Dsection'])
    def poplast3Dsection(self, root):
        if root == None:
            return None
        return int(root.attrib['last3Dsection'])
    def popmax3Dconnection(self, root):
        if root == None:
            return None
        return int(root.attrib['max3Dconnection'])
    def popupper3Dfaces(self, root):
        if root == None:
            return None
        return root.attrib['upper3Dfaces']
    def poplower3Dfaces(self, root):
        if root == None:
            return None
        return root.attrib['lower3Dfaces']
    def popfaceNormals(self, root):
        if root == None:
            return None
        return root.attrib['faceNormals']
    def popvertexNormals(self, root):
        if root == None:
            return None
        return root.attrib['vertexNormals']
    def popfacets3D(self, root):
        if root == None:
            return None
        return int(root.attrib['facets3D'])
    def popgridType(self, root):
        if root == None:
            return None
        return int(root.attrib['gridType'])
    def pophueStopWhen(self, root):
        if root == None:
            return None
        return int(root.attrib['hueStopWhen'])
    def pophueStopValue(self, root):
        if root == None:
            return None
        return int(root.attrib['hueStopValue'])
    def popsatStopWhen(self, root):
        if root == None:
            return None
        return int(root.attrib['satStopWhen'])
    def popsatStopValue(self, root):
        if root == None:
            return None
        return int(root.attrib['satStopValue'])
    def popbrightStopWhen(self, root):
        if root == None:
            return None
        return int(root.attrib['brightStopWhen'])
    def popbrightStopValue(self, root):
        if root == None:
            return None
        return int(root.attrib['brightStopValue'])
    def poptracesStopWhen(self, root):
        if root == None:
            return None
        return root.attrib['tracesStopWhen']
    def popareaStopPercent(self, root):
        if root == None:
            return None
        return int(root.attrib['areaStopPercent'])
    def popareaStopSize(self, root):
        if root == None:
            return None
        return int(root.attrib['areaStopSize'])
    def popContourMaskWidth(self, root):
        if root == None:
            return None
        return int(root.attrib['ContourMaskWidth'])
    def popsmoothingLength(self, root):
        if root == None:
            return None
        return int(root.attrib['smoothingLength'])