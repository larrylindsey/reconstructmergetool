class Contour:
    '''Contour object containing the following data: \n   Tag \n   Name \n \
  Hidden \n   Closed \n   Simplified \n   Border \n   Fill \n \
  Mode \n   Points'''
# Python Functions
    # INITIALIZE
    def __init__(self, node, imgflag=False, transform=None):
        '''Initializes the Contour object. Two different Contour objects: Image Contours and Contours \
        delineated by the imgflag parameter.'''
        self._tag = 'Contour'
        self._name = str( node.attrib['name'] )
        self._img = imgflag
        self._comment = self.popcomment(node)
        self._hidden = self.s2b(str(node.get('hidden')))
        self._closed = self.s2b(str(node.get('closed')))
        self._simplified = self.s2b(str(node.get('simplified')))
        self._mode = self.popmode(node)
        self._transform = transform
        self._border = self.popborder(node)
        self._fill = self.popfill(node)
        self._points = self.poppoints(node)
        # List of all attributes, used for creating an attribute dictionary for output (see output(self))
        self._attribs = ['name','comment','hidden','closed','simplified','mode','border','fill','points']

    # print(<Contour>) function output
    def __str__(self):
        '''Allows user to use print(<Contour>) function'''
        return 'Contour object:\n-name: '+str(self.getname())+'\n-hidden: ' \
               +str(self.gethidden())+'\n-closed: '+str(self.getclosed()) \
               +'\n-simplified: '+str(self.getsimp())+'\n-mode: '+str(self.getmode()) \
               +'\n-border: '+str(self.getbord())+'\n-fill: '+str(self.getfill()) \
               +'\n-points: '+str(self._points)+'\n'
# Helper Functions
    def s2b(self, string):
        '''Converts string to bool'''
        return string.lower() in ('true')
    def popcomment(self, node):
        '''Searches xml node for comments.'''
        if node.get('comment', None) == None:
            return None
        else:
            return node.attrib['comment']
    def pophidden(self, node):
        '''Searches xml node for hidden.'''
        if node.get('hidden', None) == None:
            return None
        elif node.attrib['hidden'].capitalize() == 'True':
            return True
        else:
            return False
    def popclosed(self, node):
        '''Searches xml node for closed.'''
        if node.get('closed', None) == None:
            return None
        elif node.attrib['closed'].capitalize() == 'True':
            return True
        else:
            return False
    def popsimplified(self, node):
        '''Searches xml node for closed.'''
        if node.get('simplified', None) == None:
            return None
        elif node.attrib['simplified'].capitalize() == 'True':
            return True
        else:
            return False
    def popmode(self, node):
        '''Searches xml node for mode.'''
        if node.get('mode', None) == None:
            return None
        else:
            return int( node.attrib['mode'] )
    def popborder(self, node):
        '''Searches xml node for border. Creates a list of floats.'''
        bord = []
        for elem in list(node.attrib['border'].split(' ')):
            bord.append(float(elem))
        return bord
    def popfill(self, node):
        '''Searches xml node for fill. Creates a list of floats.'''
        fill = []
        for elem in list(node.attrib['fill'].split(' ')):
            fill.append(float(elem))
        return fill
    def poppoints(self, node):
        '''Searches xml node for points. List of points tuples (x,y), \
        int or float depends on type in the xml node.'''
        partPoints = list(node.attrib['points'].lstrip(' ').split(','))
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
        return self._points
    def getworldpts(self):
        '''Returns world space coordinates as [ (x,y), ... ]'''
        return self._transform.worldpts(self._points)
    def getiamgepts(self): 
        '''Returns pixel space coordinates as [ (x,y), ... ]'''
        return self._transform.imgpts() 
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
        '''Returns Border attribute'''
        ret = str(self._border[0])+' '+str(self._border[1])+' '+str(self._border[2])
        return ret
    def getfill(self):
        '''Returns Fill attribute'''
        ret = str(self._fill[0])+' '+str(self._fill[1])+' '+str(self._fill[2])
        return ret
    def getxbord(self):
        '''Returns border attribute in xml output format'''
        bord = ''
        for elem in self._border:
            bord += str(elem)+' '
        return str(bord).rstrip()
    def getxfill(self):
        '''Returns fill attribute in xml output format'''
        fill = ''
        for elem in self._fill:
            fill += str(elem)+' '
        return str(fill).rstrip()
    def getxpoints(self): #===
        '''Returns Points attribute (list of strings, each consisting of two numbers \
separated by a single space)'''
        ret = ''
        for tup in self._points:
            ret += str(tup[0])+' '+str(tup[1])+', '
        return ret.rstrip()
    def getattribs(self):
        '''Returns all attributes'''
        return self._name, \
        self._comment, \
        self._hidden, \
        self._closed, \
        self._simplified, \
        self._mode, \
        self._border, \
        self._fill, \
        self._points
    def xgetattribs(self):
        '''Returns all attributes as list of strings in xml output format'''
        return str(self._name), \
        str(self._comment), \
        str(self._hidden).lower(), \
        str(self._closed).lower(), \
        str(self._simplified).lower(), \
        str(self._mode), \
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
        
