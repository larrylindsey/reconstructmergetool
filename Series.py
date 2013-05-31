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
        self.autoSaveSeries = self.s2b(root.attrib['autoSaveSeries']) #===
        self.autoSaveSection = self.s2b(root.attrib['autoSaveSection']) #===
        self.warnSaveSection = self.s2b(root.attrib['warnSaveSection']) #===
        self.beepDeleting = self.s2b(root.attrib['beepDeleting']) #===
        self.beepPaging = self.s2b(root.attrib['beepPaging']) #===
        self.hideTraces = self.s2b(root.attrib['hideTraces']) #===
        self.unhideTraces = self.s2b(root.attrib['unhideTraces']) #===
        self.hideDomains = self.s2b(root.attrib['hideDomains']) #===
        self.unhideDomains = self.s2b(root.attrib['unhideDomains']) #===
        self.useAbsolutePaths = self.s2b(root.attrib['useAbsolutePaths']) #===
        self.defaultThickness = float(root.attrib['defaultThickness']) #===
        self.zMidSection = self.s2b(root.attrib['zMidSection']) #===
        self.thumbWidth = int(root.attrib['thumbWidth']) #===
        self.thumbHeight = int(root.attrib['thumbHeight']) #===
        self.fitThumbSections = self.s2b(root.attrib['fitThumbSections']) #===
        self.firstThumbSection = int(root.attrib['firstThumbSection']) #===
        self.lastThumbSection = int(root.attrib['lastThumbSection']) #===
        self.skipSections = int(root.attrib['skipSections']) #===
        self.displayThumbContours = self.s2b(root.attrib['displayThumbContours']) #===
        self.useFlipbookStyle = self.s2b(root.attrib['useFlipbookStyle']) #===
        self.flipRate = int(root.attrib['flipRate']) #===
        self.useProxies = self.s2b(root.attrib['useProxies']) #===
        self.widthUseProxies = int(root.attrib['widthUseProxies']) #===
        self.heightUseProxies = int(root.attrib['heightUseProxies']) #===
        self.scaleProxies = float(root.attrib['scaleProxies']) #===
        self.significantDigits = int(root.attrib['significantDigits']) #===
        self.defaultBorder = self.popdefborder(root)
        self.defaultFill = self.popdeffill(root)
        self.defaultMode = int(root.attrib['defaultMode']) #===
        self.defaultName = str(root.attrib['defaultName']) #===
        self.defaultComment = str(root.attrib['defaultComment']) #===
        self.listSectionThickness = self.s2b(root.attrib['listSectionThickness']) #===
        self.listDomainSource = self.s2b(root.attrib['listDomainSource']) #===
        self.listDomainPixelsize = self.s2b(root.attrib['listDomainPixelsize']) #===
        self.listDomainLength = self.s2b(root.attrib['listDomainLength']) #===
        self.listDomainArea = self.s2b(root.attrib['listDomainArea']) #===
        self.listDomainMidpoint = self.s2b(root.attrib['listDomainMidpoint']) #===
        self.listTraceComment = self.s2b(root.attrib['listTraceComment']) #===
        self.listTraceLength = self.s2b(root.attrib['listTraceLength']) #===
        self.listTraceArea = self.s2b(root.attrib['listTraceArea']) #===
        self.listTraceCentroid = self.s2b(root.attrib['listTraceCentroid']) #===
        self.listTraceExtent = self.s2b(root.attrib['listTraceExtent']) #===
        self.listTraceZ = self.s2b(root.attrib['listTraceZ']) #===
        self.listTraceThickness = self.s2b(root.attrib['listTraceThickness']) #===
        self.listObjectRange = self.s2b(root.attrib['listObjectRange']) #===
        self.listObjectCount = self.s2b(root.attrib['listObjectCount']) #===
        self.listObjectSurfarea = self.s2b(root.attrib['listObjectSurfarea']) #===
        self.listObjectFlatarea = self.s2b(root.attrib['listObjectFlatarea']) #===
        self.listObjectVolume = self.s2b(root.attrib['listObjectVolume']) #===
        self.listZTraceNote = self.s2b(root.attrib['listZTraceNote']) #===
        self.listZTraceRange = self.s2b(root.attrib['listZTraceRange']) #===
        self.listZTraceLength = self.s2b(root.attrib['listZTraceLength']) #===
        self.borderColors = self.popbordcolors(root)
        self.fillColors = self.popfillcolors(root)
        self.offset3D = self.popoffset3D(root)
        self.type3Dobject = int(root.attrib['type3Dobject']) #===
        self.first3Dsection = int(root.attrib['first3Dsection']) #===
        self.last3Dsection = int(root.attrib['last3Dsection']) #===
        self.max3Dconnection = int(root.attrib['max3Dconnection']) #===
        self.upper3Dfaces = self.s2b(root.attrib['upper3Dfaces']) #===
        self.lower3Dfaces = self.s2b(root.attrib['lower3Dfaces']) #===
        self.faceNormals = self.s2b(root.attrib['faceNormals']) #===
        self.vertexNormals = self.s2b(root.attrib['vertexNormals']) #===
        self.facets3D = int(root.attrib['facets3D']) #===
        self.dim3D = self.popdim3D(root)
        self.gridType = int(root.attrib['gridType']) #===
        self.gridSize = self.popgridsize(root)
        self.gridDistance = self.popgriddistance(root)
        self.gridNumber = self.popgridnumber(root)
        self.hueStopWhen = int(root.attrib['hueStopWhen']) #===
        self.hueStopValue = int(root.attrib['hueStopValue']) #===
        self.satStopWhen = int(root.attrib['satStopWhen']) #===
        self.satStopValue = int(root.attrib['satStopValue']) #===
        self.brightStopWhen = int(root.attrib['brightStopWhen']) #===
        self.brightStopValue = int(root.attrib['brightStopValue']) #===
        self.tracesStopWhen = self.s2b(root.attrib['tracesStopWhen']) #===
        self.areaStopPercent = int(root.attrib['areaStopPercent']) #===
        self.areaStopSize = int(root.attrib['areaStopSize']) #===
        self.ContourMaskWidth = int(root.attrib['ContourMaskWidth']) #===
        self.smoothingLength = int(root.attrib['smoothingLength']) #===
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
        if string != None:
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