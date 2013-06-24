from shapely.geometry import Polygon, LineString, Point, box
import math
import numpy as np
class Contour:
    '''Contour object containing the following data: \n   Tag \n   Name \n \
  Hidden \n   Closed \n   Simplified \n   Border \n   Fill \n \
  Mode \n   Points'''
# Python Functions
    # INITIALIZE
    def __init__(self, node=None, imgflag=None, transform=None):
        '''Initializes the Contour object. Two different Contour objects: Image Contours and Contours \
        delineated by the imgflag parameter.'''
        self.tag = 'Contour'
        self.name = self.popname(node)
        self.img = imgflag
        self.comment = self.popcomment(node)
        self.hidden = self.s2b(str(self.pophidden(node)))
        self.closed = self.s2b(str(self.popclosed(node)))
        self.simplified = self.s2b(str(self.popsimplified(node)))
        self.mode = self.popmode(node)
        self.transform = transform
        self.border = self.popborder(node)
        self.fill = self.popfill(node)
        self.points = self.poppoints(node)
        # Private
        self._shape = None # Shapely. Populated when necessary for computation (e.g. reconstructmergetool.py)
        self._attribs = ['name','comment','hidden','closed','simplified','mode','border','fill','points'] # List of all attributes, used for creating an attribute dictionary for output (see output(self))

    # print(<Contour>) function output
    def __str__(self):
        '''Allows user to use print(<Contour>) function'''
        return 'Contour object:\n-name: '+str(self.getname())+'\n-hidden: ' \
               +str(self.gethidden())+'\n-closed: '+str(self.getclosed()) \
               +'\n-simplified: '+str(self.getsimp())+'\n-mode: '+str(self.getmode()) \
               +'\n-border: '+str(self.getbord())+'\n-fill: '+str(self.getfill()) \
               +'\n-points: '+str(self.points)+'\n'
# Helper Functions
    def overlaps(self, other):
        # Check bounding box
        if not self.box().intersects( other.box() ) and not self.box().touches( other.box() ):
#             print('ovlpscheck 1') #===
            return 0
        # Check if both same class of contours
        if self.closed != other.closed:
#             print('ovlpscheck 2') #===
            return 0
        threshold = (1+2**(-17))    
        # Closed contours
        if self.closed:
            AoU = self._shape.union( other._shape ).area
            AoI = self._shape.intersection( other._shape ).area
            if AoI == 0:
#                 print('ovlpscheck 2.5') #===
                return 0
            elif AoU/AoI > threshold:
#                 print('ovlpscheck 3') #===
                return AoU/AoI
            elif AoU/AoI < threshold:
#                 print('ovlpscheck 4') #===
                return 1
        # Open contours
        if len( self.points ) != len( other.points ):
#             print('ovlpscheck 5') #===
            return 0
        def distance(pt0, pt1):
            return math.sqrt( (pt0[0] - pt1[0])**2 + (pt0[1] - pt1[1])**2 )
        # Lists of world coords to compare
        a = self.transform.worldpts(self.points)
        b = other.transform.worldpts(other.points)
        distlist = [distance(a[i],b[i]) for i in range(len(self.points))] 
        for elem in distlist:
            if elem > threshold:
#                 print('ovlpscheck 6') #===
                return 0
        return 1
    def s2b(self, string):
        '''Converts string to bool'''
        if string == 'None':
            return None
        else:
            return string.lower() in ('true')
    def popname(self, node):
        if node == None:
            return 'Empty Contour'
        else:
            return str( node.get('name') )
    def popshape(self):
        '''Adds polygon object (shapely) to self._shape'''
        # Closed trace
        if self.closed == True:
            # If image contour, multiply pts by mag before inverting transform
            if self.img != None:
                mag = self.img.mag
                xvals = [pt[0]*mag for pt in self.points]
                yvals = [pt[1]*mag for pt in self.points]
                pts = zip(xvals,yvals)
            else:
                pts = self.points
            self._shape = Polygon( self.transform.worldpts(pts) )
        # Open trace
        elif self.closed == False and len(self.points)>1:
            self._shape = LineString( self.transform.worldpts(self.points) )
        else:
            print('\nInvalid shape characteristics: '+self.name)
            quit() # for dbugging
    def box(self):
        '''Returns bounding box of shape (shapely) library'''
        if self._shape != None:
            minx, miny, maxx, maxy = self._shape.bounds
            return box(minx, miny, maxx, maxy)
        else:
            print('NoneType for shape: '+self.name)
    def popcomment(self, node):
        '''Searches xml node for comments.'''
        if node == None:
            return None
        else:
            return node.get('comment', None)
    def pophidden(self, node):
        '''Searches xml node for hidden.'''
        if node == None:
            return None
        elif str(node.get('hidden', None)).capitalize() == 'True':
            return True
        else:
            return False
    def popclosed(self, node):
        '''Searches xml node for closed.'''
        if node == None:
            return None
        elif str(node.get('closed', None)).capitalize() == 'True':
            return True
        else:
            return False
    def popsimplified(self, node):
        '''Searches xml node for closed.'''
        if node == None:
            return None
        elif str(node.get('simplified', None)).capitalize() == 'True':
            return True
        else:
            return False
    def popmode(self, node):
        '''Searches xml node for mode.'''
        if node == None:
            return None
        else:
            return int( node.get('mode') )
    def popborder(self, node):
        '''Searches xml node for border. Creates a list of floats.'''
        if node == None:
            return []
        bord = [float(elem) for elem in list(node.get('border').split(' '))]
        return bord
    def popfill(self, node):
        '''Searches xml node for fill. Creates a list of floats.'''
        if node == None:
            return []
        fill = [float(elem) for elem in list(node.get('fill').split(' '))]
        return fill
    def poppoints(self, node):
        '''Searches xml node for points. List of points tuples (x,y), \
        int or float depends on type in the xml node.'''
        if node == None:
            return []
        partPoints = list(node.get('points').lstrip(' ').split(','))
        #make a new list of clean points, to be added to object
        ptList = []
        for i in range( len(partPoints) ):
            ptList.append( partPoints[i].strip() )
        #remove empty spots in list
        for i in range( len(ptList) ):
            if ptList[i] == '':
                ptList.remove('')
        #convert strings into tuples
        strTupList = []
        for elem in ptList:
            strTupList.append(tuple(elem.split(' ')))
        tupList = []
        for elem in strTupList:
            if '.' in elem[0]: #Float
                a=float(elem[0]) 
            if '.' in elem[1]: #Float
                b=float(elem[1])
            if '.' not in elem[0] and '.' not in elem[1]: #Int
                a=int(elem[0])
                b=int(elem[1])
            if '.' not in elem[0] and '.' in elem[1]:
                a = int(elem[0])
                b = float(elem[1])
            if '.' in elem[0] and '.' not in elem[1]:
                a = float(elem[0])
                b = int(elem[1])
            tup = (a,b)
            tupList.append(tup)
        return tupList
# Accessors
    def gettracepts(self):
        '''Returns trace space coordinates as [ (x,y), ... ]'''
        return self.points
    def getworldpts(self):
        '''Returns world space coordinates as [ (x,y), ... ]'''
        # transform.worlpts(pts) is in the form of nparray
        ptlist = [tuple(elem) for elem in self.transform.worldpts(self.points)]
        return ptlist # List of tuples
    def getiamgepts(self): 
        '''Returns pixel space coordinates as [ (x,y), ... ]'''
        return self.transform.imgpts() 
    def gettag(self):
        '''Returns Tag (str)'''
        return self.tag
    def getname(self):
        '''Returns Name attribute (str)'''
        return self.name
    def gethidden(self):
        '''Returns Hidden attribute (bool)'''
        return self.hidden
    def getclosed(self):
        '''Returns Closed attribute (bool)'''
        return self.closed
    def getsimp(self):
        '''Returns Simplified attribute (bool)'''
        return self.simplified
    def getmode(self):
        '''Returns Mode attribute (int)'''
        return self.mode
    def getbord(self):
        '''Returns Border attribute'''
        ret = str(self.border[0])+' '+str(self.border[1])+' '+str(self.border[2])
        return ret
    def getfill(self):
        '''Returns Fill attribute'''
        ret = str(self.fill[0])+' '+str(self.fill[1])+' '+str(self.fill[2])
        return ret
    def getxbord(self):
        '''Returns border attribute in xml output format'''
        bord = ''
        for elem in self.border:
            bord += str(elem)+' '
        return str(bord).rstrip()
    def getxfill(self):
        '''Returns fill attribute in xml output format'''
        fill = ''
        for elem in self.fill:
            fill += str(elem)+' '
        return str(fill).rstrip()
    def getxpoints(self): #===
        '''Returns Points attribute (list of strings, each consisting of two numbers \
separated by a single space)'''
        ret = ''
        for tup in self.points:
            ret += str(tup[0])+' '+str(tup[1])+', '
        return ret.rstrip()
    def getattribs(self):
        '''Returns all attributes'''
        return self.name, \
        self.comment, \
        self.hidden, \
        self.closed, \
        self.simplified, \
        self.mode, \
        self.border, \
        self.fill, \
        self.points
    def xgetattribs(self):
        '''Returns all attributes as list of strings in xml output format'''
        return str(self.name), \
        str(self.comment), \
        str(self.hidden).lower(), \
        str(self.closed).lower(), \
        str(self.simplified).lower(), \
        str(self.mode), \
        str(self.getxbord()), \
        str(self.getxfill()), \
        str(self.getxpoints()) 
    def output(self):
        '''Returns a dictionary of attributes'''
        attributes = {}
        keys = self._attribs
        values = list(self.xgetattribs())
        count = 0
        for value in values:
            if value not in [None, 'None', 'none']:
                attributes[keys[count]] = value
            count += 1
        return attributes
        
