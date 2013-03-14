#  Files: reconObjects.py, reconstructmergetool.py
#
#  Description: Contains the classes used for reconstructmergetool.py
#               Section, Image, Contour, Transform, ObjectList
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 3/14/2013
#
#  Currently implementing:
    #===== Add imgpts and worldpts in Contour object

    
import xml.etree.ElementTree as ET
               
class ObjectList:
    '''A list object containing multiple objects.'''
    # Python functions
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
        elif x > (len(self)-1):
            print( 'Invalid argument. x is outside of list range.')

    # Mutators
    def addO(self, O):
        '''Appends an object to <ObjectList>.'''
        self._list.append(O)
        self._len += 1
    def removeO(self, O):
        '''Removes an object from <ObjectList>.'''
        self._list.remove(O)
        self._len -= 1


        
class xmlTree:
    '''ElementTree containing XML data from <path>'''
    # Python Functions 
    def __init__(self, path):
        self._name = str( path.rpartition('/')[2] ) #name = name of xml file
        self._tree = ET.parse(path)

    # Accessors
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
    def chgname(self, x):
        self._name = str(x)
    def chgtree(self, x):
        '''Needs to be an ET.parse(<xmlfile>) class.'''
        self._tree = x


    
class Section:
    '''<Section> is an object with attributes: index, thickness, alignLocked \
as well as a list containing <image> and <contour> objects.'''
    # Python Functions
    def __init__(self, xmlTree):
        # Create <section>
        self._list = ObjectList()
        # Create <section> attributes
        self._index = xmlTree.getsection()[0]
        self._thick = xmlTree.getsection()[1]
        self._alignLock = xmlTree.getsection()[2]
    def __len__(self):
        '''Allows use of len(<section>) function. Returns length'''
        return len(self._list)
    def __getitem__(self,x):
        return self._list[x]
    def __str__(self):
        '''Allows use of print(<section>) function.'''
        return 'Index: %d\nThickness: %f\nAlign Locked: %s'%(self._index, \
                                                               self._thick, \
                                                        self._alignLock)    
    # Accessors
    def getindex(self):
        return self._index
    def getthickness(self):
        return self._thick
    def getalignlock(self):
        return self._alignLock

    # Mutators
    def chgindex(self, x):
        self._index = int(x)
    def chgthickness(self, x):
        self._thick = float(x)
    def chgalignlock(self, x):
        self._alignLock = bool(x)


        
class Image:
    '''Image object containing the following attributes: src (string), mag (float), \
contrast (float), brightness (float), red (bool), green (bool), blue (bool), and \
transform (object)'''
    # Python functions
    def __init__(self, node, transform):
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
        return self._trnsfrm #====
    def getattribs(self):
        '''Returns all attributes for <image>'''
        return self.getsrc(), self.getmag(), self.getcontrast(), \
               self.getbrightness(), self.getred(), self.getgreen(), \
               self.getblue(), self.gettransform()

    # Mutators
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


    
class Transform:
    '''Transform object containing the following data: \n   Dim \n \
  yCoef \n   xCoef'''

    # Python functions
    def __init__(self, node):
        '''Initializes the Transform object'''
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
        '''Allows user to use print( <Transformobject> ) function'''
        return 'Transform object:\nDim: '+str(self.getDim())+'\nYcoef: ' \
               +str(self.getycoef())+'\nXcoef: '+str(self.getxcoef())+'\n'

    # Accessors 
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
    def chgdim(self, x):
        self._dim = int(x)
    def chgycoef(self, x):
        self._ycoef = list(x)
    def chgxcoef(self, x):
        self._xcoef = list(x)



class Contour:
    '''Contour object containing the following data: \n   Name \n \
  Hidden \n   Closed \n   Simplified \n   Border \n   Fill \n \
  Mode \n   Points'''
    # Python Functions
    def __init__(self, node, transform):
        '''Initializes the Contour object'''
        self._name = str( node.attrib['name'] )
        self._hidden = bool( node.attrib['hidden'].capitalize() )
        self._closed = bool( node.attrib['closed'].capitalize() )
        self._simplified = bool( node.attrib['closed'].capitalize() )
        self._mode = int( node.attrib['mode'] )
        self._transform = transform
        self._border = []
        self._fill = []
        self._points = []
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
        return 'Contour object:\nName: '+str(self.getname())+'\nHidden: ' \
               +str(self.gethidden())+'\nClosed: '+str(self.getclosed()) \
               +'\nSimplified: '+str(self.getsimp())+'\nMode: '+str(self.getmode()) \
               +'\nBorder: '+str(self.getbord())+'\nFill: '+str(self.getfill()) \
               +'\nPoints: '+str(self.getpoints())+'\n'

    # Accessors 
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
