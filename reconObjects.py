#  Files: reconObjects.py, reconstructmergetool.py
#
#  Description: Contains the classes used for reconstructmergetool.py
#               Section, Image, Contour, Transform, ObjectList
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 3/13/2013
#
#  Currently implementing:
    #===== shorten addOfromFile() function in objectList class (or delete?)
    #===== Add imgpts and worldpts in Contour object
    #===== make less redundant
    #===== print fxns (cont) need to print all attributes
    

import xml.etree.ElementTree as ET
        
class xmlTree:
    '''ElementTree containing XML data from <path>'''
    def __init__(self, path):
        self._name = str( path.rpartition('/')[2] ) #name = name of xml file
        self._tree = ET.parse(path)

    def getsection(self):
        '''Returns <section> attributes as a triple (index(int), \
alignLocked(bool), thickness(float).'''
        return int(self._tree.getroot().attrib['index']), \
               float(self._tree.getroot().attrib['thickness']), \
               bool(self._tree.getroot().attrib['alignLocked'])

    def gettreelist(self):
        '''Returns xmlTree as a list object'''
        return list( self._tree.iter() )
               
class ObjectList:
    '''A list object containing multiple objects.'''
    def __init__(self):
        '''Creates empty ObjectList.'''
        self._list = []
        self._len = 0

    def __len__(self):
        '''Allows use of len( <ObjectList> ) function. \
Returns the number of objects in the ObjectList.'''
        return self._len

    def __getitem__(self, x):
        '''Allows the use of <ObjectList>[x] function. \
Returns xth item from the ObjectList'''
        if x <= (len(self)-1): #===================== need to double check
            return self._list[x]
        else:
            print( 'Invalid argument. x is outside of list range.')
    
    def isEmpty(self):
        '''Return True (bool) if <ObjectList> is empty.'''
        return self._len == 0
        
    def addO(self, O):
        '''Appends an object to the <ObjectList>.'''
        self._list.append(O)
        self._len += 1
        
class Section:
    '''<Section> is an object with attributes: index, thickness, alignLocked \
as well as a list containing <image> and <contour> objects.'''
    
    def __init__(self, xmlTree):
        # Create <section>
        self._list = ObjectList()

        # Create <section> attributes
        self._index = xmlTree.getsection()[0]
        self._thick = xmlTree.getsection()[1]
        self._alignLock = xmlTree.getsection()[2]

    # Python functions
    def __len__(self):
        '''Allows use of len(<section>) function.\
Returns length of <section>'''
        return len(self._list)
    def __str__(self):
        '''Allows use of print(<section>) function.'''
        return 'Index: %d\nThickness: %f\nAlign Locked: %s'%(self._index, \
                                                               self._thick, \
                                                               self._alignLock)
    def __getitem__(self,x):
        return self._list[x]
    
    # Accessors
    def getindex(self):
        return self._index
    def getthickness(self):
        return self._thick
    def getalignlock(self):
        return self._alignLock
        
        
class Image: #=================================
    def __init__(self, node, transform): #===========
        self._src = node.attrib['src']
        self._mag = float( node.attrib['mag'] )
        self._cntrst = float( node.attrib['contrast'] )
        self._bright = float( node.attrib['brightness'] )
        self._red = bool( node.attrib['red'].capitalize() )
        self._green = bool( node.attrib['green'].capitalize() )
        self._blue = bool( node.attrib['blue'].capitalize() )
        self._trnsfrm = transform

    def __str__(self):
        return 'src: %s\nmag: %f\ncontrast: %f\nbrightness: %f\n\
red: %s\ngreen: %s\nblue: %s\ntransform: %s'%self.getattribs() #================

    # Accessors 
    def getsrc(self):
        return self._src
    def getmag(self):
        return self._mag
    def getcontrast(self):
        return self._cntrst
    def getbrightness(self):
        return self._bright
    def getred(self):
        return self._red
    def getgreen(self):
        return self._green
    def getblue(self):
        return self._blue
    def gettransform(self):
        return self._trnsfrm
    def getattribs(self):
        '''Returns all attributes for <image>'''
        return self.getsrc(), self.getmag(), self.getcontrast(), \
               self.getbrightness(), self.getred(), self.getgreen(), \
               self.getblue(), self.gettransform()

        
class Transform:
    '''Transform object containing the following data: \n   Dim \n \
  yCoef \n   xCoef'''

    def __init__(self, node):
        '''Initializes the Transform object'''
        self._dim = node.attrib['dim']
        self._ycoef = []
        self._xcoef = []
        
        # Populate ycoef/xcoef lists
        for char in node.attrib['ycoef']:
            if char.isdigit():
                self._ycoef.append( int(char) )

        for char in node.attrib['xcoef']:
            if char.isdigit():
                self._xcoef.append( int(char) )

    def __str__(self):
        '''Allows user to use print( <Transformobject> ) function'''
        return 'Transform object:\nDim: '+str(self.getDim())+'\nYcoef: ' \
               +str(self.getycoef())+'\nXcoef: '+str(self.getxcoef())+'\n'

    # Accessors 
    def getDim(self):
        '''Returns Dim (int)'''
        return self._dim
    def getycoef(self):
        '''Returns ycoefs (list of ints)'''
        return self._ycoef
    def getxcoef(self):
        '''Returns xcoefs (list of ints)'''
        return self._xcoef
    def getAttribs(self):
        '''Returns Dim, ycoefs, and xcoefs'''
        return self.getDim(), self.getycoef(), self.getxcoef()

class Contour:
    '''Contour object containing the following data: \n   Name \n \
  Hidden \n   Closed \n   Simplified \n   Border \n   Fill \n \
  Mode \n   Points'''

    def __init__(self, node, transform):
        '''Initializes the Contour object'''
    # Variables
        # Variables created directly from parameters
        self._name = str( node.attrib['name'] )
        self._hidden = bool( node.attrib['hidden'].capitalize() )
        self._closed = bool( node.attrib['closed'].capitalize() )
        self._simplified = bool( node.attrib['closed'].capitalize() )
        self._mode = int( node.attrib['mode'] )
        self._transform = transform
        # Variables created after processing parameters ===============
        self._border = []
        self._fill = []
        self._points = []
            #border
        for char in node.attrib['border']:
            if char.isdigit():
                self._border.append( int(char) )
            #fill
        for char in node.attrib['fill']:
            if char.isdigit():
                self._fill.append( int(char) )
            #points
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

    def __str__(self):
        '''Allows user to use print( <Contourobject> ) function'''
        return 'Contour object:\nName: '+str(self.getName())+'\nHidden: ' \
               +str(self.getHidden())+'\nClosed: '+str(self.getClosed()) \
               +'\nSimplified: '+str(self.getSimp())+'\nMode: '+str(self.getMode()) \
               +'\nBorder: '+str(self.getBord())+'\nFill: '+str(self.getFill()) \
               +'\nPoints: '+str(self.getPoints())+'\n'

    # Accessors 
    def getName(self):
        '''Returns Name attribute (str)'''
        return self._name
    def getHidden(self):
        '''Returns Hidden attribute (bool)'''
        return self._hidden
    def getClosed(self):
        '''Returns Closed attribute (bool)'''
        return self._closed
    def getSimp(self):
        '''Returns Simplified attribute (bool)'''
        return self._simplified
    def getMode(self):
        '''Returns Mode attribute (int)'''
        return self._mode
    def getBord(self):
        '''Returns Border attribute (list of ints)'''
        return self._border
    def getFill(self):
        '''Returns Fill attribute (list of ints)'''
        return self._fill
    def getPoints(self):
        '''Returns Points attribute (list of strings, each consisting of two numbers \
separated by a single space)'''
        return self._points
    def getAttribs(self):
        '''Returns all contour attributes'''
        return self.getName(), self.getHidden(), self.getClosed(), self.getSimp(), \
               self.getMode(), self.getBord(), self.getFill(), self.getPoints



##    def addOfromFile(self, path, objType): #===delete?
##        '''Parses XML file (path), creates a <objType> object, adds the objects to ObjectList.'''
##        #parse xml
##        tree = ET.parse(path)
##        root = tree.getroot() #Section = root.tag, Transform = root, contour = root[x]
##
##        #list of all elements in XML doc
##        allList = list( tree.iter() )
##
##        #go through allList, make object, add object to ObjectList
##        objType = str(objType).capitalize()
##
##        for elem in allList:
##            # Transform loop
##            if objType == 'Transform' and elem.tag == 'Transform':
##                O = Transform(elem.attrib['dim'], elem.attrib['ycoef'], elem.attrib['xcoef'])
##                self.addO(O)
##
##            # Contour loop
##            elif objType == 'Contour' and elem.tag == 'Contour':
##                #partition points into a list of messy crap
##                partPoints = list(elem.attrib['points'].lstrip(' ').split(','))
##
##                #make a new list of clean points, to be added to object
##                ptList = []
##                for i in range( len(partPoints) ):
##                    ptList.append( partPoints[i].strip() )
##
##                #remove empty points
##                for i in range( len(ptList) ):
##                    if ptList[i] == '':
##                        ptList.remove('')
##                
##                O = Contour(elem.attrib['name'], elem.attrib['hidden'], elem.attrib['closed'], \
##                            elem.attrib['simplified'], elem.attrib['border'], elem.attrib['fill'], \
##                            elem.attrib['mode'], ptList)
##                self.addO(O)
