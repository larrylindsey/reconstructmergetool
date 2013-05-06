class ZContour:
    '''Creates a <serContour> object which represents Contours and ZCountours in /
a .ser file. Contour and ZContour can be distinguished by tags.'''
# Python Functions
    # INITIALIZE
    def __init__(self, node):
        self._tag = 'ZContour'
        self._name = str( node.attrib['name'] )
        self._closed = self.s2b(str(node.get('closed')))
        self._mode = self.popmode(node)
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
    def getpoints(self):
        '''Returns Points attribute (list of strings, each consisting of two numbers \
separated by a single space)'''
        return self._points
    def getxbord(self):
        bord = ''
        for elem in self._border:
            bord += str(elem)+' '
        return str(bord).rstrip()
    def getxfill(self):
        fill = ''
        for elem in self._fill:
            fill += str(elem)+' '
        return str(fill).rstrip()
    def getxpoints(self):
        ret = ''
        for tup in self._points:
            ret += tup+', '
        return ret.rstrip()
    def getattribs(self):
        '''Returns all zcontour attributes'''
        return self._name, self._closed, self._border, self._fill, \
               self._mode, self._points
    def xgetattribs(self):
        '''Returns all zcontour attributes, xml formatting (strings)'''
        return str(self._name), str(self._closed).lower(), self.getxbord(), self.getxfill(), \
            str(self._mode), str(self.getxpoints())
    def output(self): #===
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
# Mutators
    def s2b(self, string):
        '''Converts string to bool'''
        return string.lower() in ('true')
    def popmode(self, node):
        if node.get('mode', None) == None:
            return None
        else:
            return int( node.attrib['mode'] )
    def popborder(self, node):
        '''Populates self._border'''
        bord = []
        for elem in list(node.attrib['border'].split(' ')):
            bord.append(float(elem))
        return bord
    def popfill(self, node):
        '''Populates self._fill'''
        fill = []
        for elem in list(node.attrib['fill'].split(' ')):
            fill.append(float(elem))
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