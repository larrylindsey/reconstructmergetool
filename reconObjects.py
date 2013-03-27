#  Files: reconObjects.py, reconstructmergetool.py, transform.py
#
#  Description: Contains the classes used for reconstructmergetool.py
#               Section, Image, Contour, Transform, ObjectList
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 3/26/2013
#
#  Currently working on: **Search for '===' to find important/unstable code
    #===== Add imgpts and worldpts in Contour object (scimage.transform)
    #===== Check comments on classes

    
import xml.etree.ElementTree as ET
from scimage import transfrom as TF

#############################################################################               
class ObjectList:
    '''A list object containing multiple objects.'''
    # Python functions
    def __init__(self):
        '''Creates empty ObjectList.'''
        self._tag = 'ObjectList'
        self._list = []
        self._len = 0
    def __len__(self):
        '''Allows use of len( <ObjectList> ) function. \
Returns the number of objects in the ObjectList.'''
        return self._len
    def __getitem__(self, x):
        '''Allows the use of <ObjectList>[x] function. \
Returns xth item from the ObjectList'''
        if x <= (len(self)-1):
            return self._list[x]
    def __str__(self):
        '''Allows use of print( <ObjectList> ) function.'''
        taglist = []
        for i in range(len(self)):
            taglist.append( self._list[i].gettag() )
        return str(taglist)
    
    # Accessors
    def gettag(self):
        return self._tag
        
    # Mutators
    def addO(self, O):
        '''Appends an object to <ObjectList>.'''
        self._list.append(O)
        self._len += 1
    def removeO(self, O):
        '''Removes an object from <ObjectList>.'''
        self._list.remove(O)
        self._len -= 1
    def chgtag(self, x):
        self._tag = str(x)


#############################################################################         
class xmlTree:
    '''ElementTree containing XML data from <path>'''
    # Python Functions 
    def __init__(self, path):
        self._tag = 'xmltree'
        self._name = str( path.rpartition('/')[2] ) #name = name of xml file
        self._tree = ET.parse(path) #object containing data
        self._treelist = self.gettreelist() #data in _tree stored as a list
    # Accessors
    def gettag(self):
        return self._tag
    def getsection(self):
        '''Returns <section> attributes as a triple (index(int), \
alignLocked(bool), thickness(float).'''
        return int(self._tree.getroot().attrib['index']), \
               float(self._tree.getroot().attrib['thickness']), \
               bool(self._tree.getroot().attrib['alignLocked'])
    def gettreelist(self):
        '''Returns xmlTree as a list object'''
        return list( self._tree.iter() )

    # Mutators
    def chgtag(self, x):
        self._tag = str(x)
    def chgname(self, x):
        self._name = str(x)
    def chgtree(self, x):
        '''Needs to be an ET.parse(<xmlfile>) class.'''
        self._tree = x


#############################################################################
class Series:
    '''<Series> is an object with attributes: name \
as well as a list containing all of the <Sections> objects associated with
it'''
    #Python functions
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
        
        
	
    def __getitem__(self,x):
        '''Allows use of <Section>[x] to return xth elements in list'''
        return self._list[x]
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

#############################################################################    
class Section:
    '''<Section> is an object with attributes: index, thickness, alignLocked \
as well as a list containing <image> and <contour> objects. \
Attributes printed with print(<section>) objects in list printed with print(<section>._list)'''
    # Python Functions
    def __init__(self, xmlTree):
        # Create <section>
        self._name = xmlTree._name
        self._list = ObjectList()
        self._tag = 'Section'
        # Create <section> attributes
        self._index = xmlTree.getsection()[0]
        self._thick = xmlTree.getsection()[1]
        self._alignLock = xmlTree.getsection()[2]
        # Populate section with image, contour and transforms
        tmpT = '' #current transform
        for node in xmlTree.gettreelist():
            if node.tag == 'Transform':
                tmpT = Transform(node)
            elif node.tag == 'Image':
                I = Image(node, tmpT)
                self._list.addO(I)
            elif node.tag == 'Contour':
                C = Contour(node, tmpT)
                self._list.addO(C)
            elif node.tag == 'ZContour': #=========
                Z = ZContour(node, tmpT)
                self._list.addO(Z)
    def __len__(self):
        '''Allows use of len(<Section>) function. Returns length'''
        return len(self._list)
    def __getitem__(self,x):
        '''Allows use of <Section>[x] to return xth elements in list'''
        return self._list[x]
    def __str__(self):
        '''Allows use of print(<section>) function.'''
        return 'Index: %d\nThickness: %f\nAlign Locked: %s'%(self._index, \
                                                                 self._thick, \
                                                                 self._alignLock)     
    # Accessors
    def gettag(self):
        '''--> (str)'''
        return self._tag
    def getindex(self):
        '''--> (int)'''
        return self._index
    def getthickness(self):
        '''--> (float)'''
        return self._thick
    def getalignlock(self):
        '''--> (bool)''' 
        return self._alignLock

    # Mutators
    def chgtag(self, x):
        self._tag = str(x)
    def chgindex(self, x):
        self._index = int(x)
    def chgthickness(self, x):
        self._thick = float(x)
    def chgalignlock(self, x):
        self._alignLock = bool(x)
    def chgtag(self, x):
        self._tag = str(x)
        

#############################################################################        
class Image:
    '''Image object containing the following attributes: src (string), mag (float), \
contrast (float), brightness (float), red (bool), green (bool), blue (bool), and \
transform (object)'''
    # Python functions
    def __init__(self, node, transform):
        self._tag = 'Image'
        self._src = node.attrib['src']
        self._mag = float( node.attrib['mag'] )
        self._cntrst = float( node.attrib['contrast'] )
        self._bright = float( node.attrib['brightness'] )
        self._red = bool( node.attrib['red'].capitalize() )
        self._green = bool( node.attrib['green'].capitalize() )
        self._blue = bool( node.attrib['blue'].capitalize() )
        self._trnsfrm = transform
    def __str__(self):
        '''Allows print( <image> ) function. Returns attributes as string.'''
        return 'Image Object:\n-src: %s\n-mag: %f\n-contrast: %f\n-brightness: %f\n\
-red: %s\n-green: %s\n-blue: %s\n-%s'%(self.getattribs())

    # Accessors
    def gettag(self):
        '''tag ---> string'''
        return self._tag
    def getsrc(self):
        '''src ---> string'''
        return self._src
    def getmag(self):
        '''mag ---> float'''
        return self._mag
    def getcontrast(self):
        '''contrast ---> float'''
        return self._cntrst
    def getbrightness(self):
        '''brightness ---> float'''
        return self._bright
    def getred(self):
        '''red ---> bool'''
        return self._red
    def getgreen(self):
        '''green ---> bool'''
        return self._green
    def getblue(self):
        '''blue ---> bool'''
        return self._blue
    def gettransform(self):
        '''transform ---> object'''
        return self._trnsfrm
    def getattribs(self):
        '''Returns all attributes for <image>'''
        return self.getsrc(), self.getmag(), self.getcontrast(), \
               self.getbrightness(), self.getred(), self.getgreen(), \
               self.getblue(), self.gettransform()

    # Mutators
    def chgtag(self, x):
        self._tag = str(x)
    def chgsrc(self, x):
        self._src = str(x)  
    def chgmag(self, x):
        self._mag = float(x)
    def chgcontrast(self, x):
        self._cntrst = float(x)
    def chgbrightness(self, x):
        self._bright = float(x)
    def chgred(self, x):
        self._red = bool(x)
    def chggreen(self, x):
        self._green = bool(x)
    def chgblue(self, x):
        self._blue = bool(x)
    def chgtransform(self, x):
        self._trnsfrm = x


#############################################################################     
class Transform:
    '''Transform object containing the following data: \n   Dim \n \
  yCoef \n   xCoef'''
    # Python functions
    def __init__(self, node):
        '''Initializes the Transform object'''
        self._tag = 'Transform'
        self._dim = node.attrib['dim']
        self._ycoef = []
        self._xcoef = []
        # Populate y/xcoefs
        for char in node.attrib['ycoef']:
            if char.isdigit():
                self._ycoef.append( int(char) )
        for char in node.attrib['xcoef']:
            if char.isdigit():
                self._xcoef.append( int(char) )
    def __str__(self):
        '''Allows user to use print( <Transform> ) function'''
        return 'Transform object:\n-dim: '+str(self.getdim())+'\n-ycoef: ' \
               +str(self.getycoef())+'\n-xcoef: '+str(self.getxcoef())+'\n'

    # Accessors
    def gettag(self):
        '''Returns tag (string)'''
        return self._tag
    def getdim(self):
        '''Returns Dim (int)'''
        return self._dim
    def getycoef(self):
        '''Returns ycoefs (list of ints)'''
        return self._ycoef
    def getxcoef(self):
        '''Returns xcoefs (list of ints)'''
        return self._xcoef
    def getattribs(self):
        '''Returns Dim, ycoefs, and xcoefs'''
        return self.getDim(), self.getycoef(), self.getxcoef()

    # Mutators
    def chgtag(self, x):
        self._tag = str(x)
    def chgdim(self, x):
        self._dim = int(x)
    def chgycoef(self, x):
        self._ycoef = list(x)
    def chgxcoef(self, x):
        self._xcoef = list(x) 


############################################################################# 
class Contour:
    '''Contour object containing the following data: \n   Tag \n   Name \n \
  Hidden \n   Closed \n   Simplified \n   Border \n   Fill \n \
  Mode \n   Points'''
    # Python Functions
    def __init__(self, node, transform=None): #=====
        '''Initializes the Contour object'''
        if transform == None: #Contours in .ser files
            self._tag = 'Contour'
            self._name = str( node.attrib['name'] )
            self._closed = bool( node.attrib['closed'].capitalize() )
            self._mode = int( node.attrib['mode'] )
            self._border = []
            self._fill = []
            self._points = []
        else: #Contours in .xml files
            self._tag = 'Contour'
            self._name = str( node.attrib['name'] )
            self._hidden = bool( node.attrib['hidden'].capitalize() )
            self._closed = bool( node.attrib['closed'].capitalize() )
            self._simplified = bool( node.attrib['closed'].capitalize() )
            self._mode = int( node.attrib['mode'] )
            self._transform = transform
            self._border = []
            self._fill = []
            self._points = [] #List of strings. In each string are two values separate by space
        # Populate border, fill, points
        for char in node.attrib['border']:
            if char.isdigit():
                self._border.append( int(char) )
        for char in node.attrib['fill']:
            if char.isdigit():
                self._fill.append( int(char) )
            #partition points into a list of messy crap
        partPoints = list(node.attrib['points'].lstrip(' ').split(','))
            #make a new list of clean points, to be added to object
        ptList = []
        for i in range( len(partPoints) ):
            ptList.append( partPoints[i].strip() )
            #remove empty points
        for i in range( len(ptList) ):
            if ptList[i] == '':
                ptList.remove('')
        self._points = ptList
    def __str__(self):
        '''Allows user to use print( <Contourobject> ) function'''
        return 'Contour object:\n-name: '+str(self.getname())+'\n-hidden: ' \
               +str(self.gethidden())+'\n-closed: '+str(self.getclosed()) \
               +'\n-simplified: '+str(self.getsimp())+'\n-mode: '+str(self.getmode()) \
               +'\n-border: '+str(self.getbord())+'\n-fill: '+str(self.getfill()) \
               +'\n-points: '+str(self.getpoints())+'\n'

    # Accessors
    def gettag(self):
        '''Returns Tag (str)'''
        return self._tag
    def getname(self):
        '''Returns Name attribute (str)'''
        return self._name
    def gethidden(self):
        '''Returns Hidden attribute (bool)'''
        return self._hidden
    def getclosed(self):
        '''Returns Closed attribute (bool)'''
        return self._closed
    def getsimp(self):
        '''Returns Simplified attribute (bool)'''
        return self._simplified
    def getmode(self):
        '''Returns Mode attribute (int)'''
        return self._mode
    def getbord(self):
        '''Returns Border attribute (list of ints)'''
        return self._border
    def getfill(self):
        '''Returns Fill attribute (list of ints)'''
        return self._fill
    def getpoints(self):
        '''Returns Points attribute (list of strings, each consisting of two numbers \
separated by a single space)'''
        return self._points
    def getattribs(self):
        '''Returns all contour attributes'''
        return self.getname(), self.gethidden(), self.getclosed(), self.getsimp(), \
               self.getmode(), self.getbord(), self.getfill(), self.getpoints

    # Mutators
    def chgtag(self, x):
        self._tag = str(x)
    def chgname(self, x):
        self._name = str(x)
    def chghidden(self, x):
        self._hidden = bool(x)
    def chgclosed(self, x):
        self._closed = bool(x)
    def chgsimp(self, x):
        self._simplified = bool(x)
    def chgmode(self, x):
        self._mode = int(x)
    def chgbord(self, x):
        '''List of ints'''
        self._border = list(x)
    def chgfill(self, x):
        '''List of ints'''
        self._fill = list(x)
    def chgpoints(self, x):
        '''List of strings'''
        self._points = list(x)

#############################################################################
class ZContour:
    '''Creates a <serContour> object which represents Contours and ZCountours in /
a .ser file. Contour and ZContour can be distinguished by tags.'''
    # Python Functions
    def __init__(self, node):
        self._tag = 'ZContour'
        self._name = str( node.attrib['name'] )
        self._closed = bool( node.attrib['closed'].capitalize() )
        self._mode = int( node.attrib['mode'] )
        self._border = []
        self._fill = []
        self._points = [] #List of strings. Each string contains 3 numbers: 'float, float, section'
        # Populate border, fill, points
        for char in node.attrib['border']:
            if char.isdigit():
                self._border.append( float(char) )
        for char in node.attrib['fill']:
            if char.isdigit():
                self._fill.append( float(char) )

            #partition points into a list of messy crap
        partPoints = list(node.attrib['points'].lstrip(' ').split(','))
            #example: ['5.93694 3.75884 156', '  5.46795 4.10569 144',
            #'  4.82797 4.41347 139', '  4.77912 4.64308 124', '  4.63744 4.97528 99', '  ']

            #make a new list of clean points, to be added to object
        ptList = []
        for i in range( len(partPoints) ):
            ptList.append( partPoints[i].strip() )
                #example: ['5.93694 3.75884 156', '5.46795 4.10569 144', '4.82797 4.41347 139',
                #'4.77912 4.64308 124', '4.63744 4.97528 99', '']

            #remove empty points
        for i in range( len(ptList) ):
            if ptList[i] == '':
                ptList.remove('')
                #example: ['5.93694 3.75884 156', '5.46795 4.10569 144', '4.82797 4.41347 139',
                #'4.77912 4.64308 124', '4.63744 4.97528 99']
        self._points = ptList
    def __str__(self):
        '''Allows user to use print( <ZContour> ) function'''
        return 'Contour object:\n-name: '+str(self.getname())+'\n-closed: ' \
               +str(self.getclosed())+'\n-mode: '+str(self.getmode()) \
               +'\n-border: '+str(self.getbord())+'\n-fill: '+str(self.getfill()) \
               +'\n-points: '+str(self.getpoints())+'\n'

    # Accessors
    def gettag(self):
        '''Returns Tag (str)'''
        return self._tag
    def getname(self):
        '''Returns Name attribute (str)'''
        return self._name
    def getclosed(self):
        '''Returns Closed attribute (bool)'''
        return self._closed
    def getmode(self):
        '''Returns Mode attribute (int)'''
        return self._mode
    def getbord(self):
        '''Returns Border attribute (list of ints)'''
        return self._border
    def getfill(self):
        '''Returns Fill attribute (list of ints)'''
        return self._fill
    def getpoints(self):
        '''Returns Points attribute (list of strings, each consisting of two numbers \
separated by a single space)'''
        return self._points
    def getattribs(self):
        '''Returns all contour attributes'''
        return self.getname(), self.getclosed(), self.getmode(), self.getbord(), \
               self.getfill(), self.getpoints

    # Mutators
    def chgtag(self, x):
        self._tag = str(x)
    def chgname(self, x):
        self._name = str(x)
    def chgclosed(self, x):
        self._closed = bool(x)
    def chgmode(self, x):
        self._mode = int(x)
    def chgbord(self, x):
        '''List of ints'''
        self._border = list(x)
    def chgfill(self, x):
        '''List of ints'''
        self._fill = list(x)
    def chgpoints(self, x):
        '''List of strings'''
        self._points = list(x)        
        self._tag = 'ZContour'
