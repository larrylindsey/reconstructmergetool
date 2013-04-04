class Contour:
    '''Contour object containing the following data: \n   Tag \n   Name \n \
  Hidden \n   Closed \n   Simplified \n   Border \n   Fill \n \
  Mode \n   Points'''
# Python Functions
    # INITIALIZE
    def __init__(self, node, transform=None):
        '''Initializes the Contour object. Attributes vary depending on file type (.ser vs .xml).'''
        if transform == None: # Contours in .ser files dont have transform objects
            self._tag = 'Contour'
            self._name = str( node.attrib['name'] )
            self._closed = bool( node.attrib['closed'].capitalize() )
            self._mode = int( node.attrib['mode'] )
            self._transform = None
            self._border = []
            self._fill = []
            self._points = [] # [(int, int), ...]
            self._attribs = ['name','closed','border','fill','mode','points']
        else: # Contours in .xml files
            self._tag = 'Contour'
            self._name = str( node.attrib['name'] )
            self._hidden = bool( node.attrib['hidden'].capitalize() )
            self._closed = bool( node.attrib['closed'].capitalize() )
            self._simplified = bool( node.attrib['closed'].capitalize() )
            self._mode = int( node.attrib['mode'] )
            self._transform = transform # Transform object
            self._border = self.popborder(node)
            self._fill = self.popfill(node)
            self._points = self.poppoints(node) # [(float, float), ...]
            self._attribs = ['name','hidden','closed','simplified','border','fill','mode','points']
    # STRING REPRESENTATION
    def __str__(self):
        '''Allows user to use print(<Contour>) function'''
        return 'Contour object:\n-name: '+str(self.getname())+'\n-hidden: ' \
               +str(self.gethidden())+'\n-closed: '+str(self.getclosed()) \
               +'\n-simplified: '+str(self.getsimp())+'\n-mode: '+str(self.getmode()) \
               +'\n-border: '+str(self.getbord())+'\n-fill: '+str(self.getfill()) \
               +'\n-points: '+str(self.getpoints())+'\n'+str(self._transform)+'\n'

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
    def getpoints(self):
        '''Returns Points attribute (list of strings, each consisting of two numbers \
separated by a single space)'''
        ret = ''
        for tup in self._points:
            ret += str(tup[0])+' '+str(tup[1])+', '
        return ret
    def getattribs(self):
        '''Returns all contour attributes (as string) XML OUTPUT FORMATTING'''
        return str(self.getname()), str(self.gethidden()).lower(), str(self.getclosed()).lower(), str(self.getsimp()).lower(), \
               str(self.getbord()), str(self.getfill()), str(self.getmode()), str(self.getpoints())

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
    def popborder(self, node):
        '''Populates self._border'''
        bord = []
        for char in node.attrib['border']:
            if char.isdigit():
                bord.append( int(char) )
        return bord
    def popfill(self, node):
        '''Populates self._fill'''
        fill = []
        for char in node.attrib['fill']:
            if char.isdigit():
                fill.append( int(char) )
        return fill
    def poppoints(self, node):
        '''Populates self._points'''
        partPoints = list(node.attrib['points'].lstrip(' ').split(','))
        #make a new list of clean points, to be added to object
        ptList = []
        for i in range( len(partPoints) ):
            ptList.append( partPoints[i].strip() )
        #remove empty points
        for i in range( len(ptList) ):
            if ptList[i] == '':
                ptList.remove('') 
        #convert strings into tuples
        strTupList = []
        for elem in ptList:
            strTupList.append(tuple(elem.split(' ')))
        tupList = []
        for elem in strTupList:
            if '.' in elem[0]: #for floats
                a=float(elem[0])
                b=float(elem[1])
                tup = (a,b)
                tupList.append(tup)
            else: #for ints
                a=int(elem[0])
                b=int(elem[1])
                tup = (a,b)
                tupList.append(tup)
        return tupList