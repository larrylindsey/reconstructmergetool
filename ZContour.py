class ZContour:
    '''Creates a <serContour> object which represents Contours and ZCountours in /
a .ser file. Contour and ZContour can be distinguished by tags.'''
# Python Functions
    # INITIALIZE
    def __init__(self, node):
        self._tag = 'ZContour'
        self._name = str( node.attrib['name'] )
        self._closed = bool( node.attrib['closed'].capitalize() )
        self._mode = int( node.attrib['mode'] )
        self._border = self.popborder(node)
        self._fill = self.popfill(node)
        self._points = self.poppts(node) #List of strings. Each string contains 3 numbers: 'float, float, section'
        self._attribs = ['name','closed','border','fill','mode','points']
    # STRING REPRESENTATION
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
    def popborder(self, node): #======
        '''Populates self._border'''
        bord = []
        for char in node.attrib['border']:
            if char.isdigit():
                bord.append( float(char) )
        return bord
    def popfill(self, node): #=====
        '''Populates self._fill'''
        fill = []
        for char in node.attrib['fill']:
            if char.isdigit():
                fill.append( float(char) )
        return fill
    def poppts(self, node):
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
        return ptList