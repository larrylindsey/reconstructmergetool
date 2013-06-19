class ZContour:
    '''Creates a <serContour> object which represents Contours and ZCountours in /
a .ser file. Contour and ZContour can be distinguished by tags.'''
# Python Functions
    # INITIALIZE
    def __init__(self, node=None):
        self.tag = 'ZContour'
        self.name = self.popname(node)
        self.closed = self.s2b(self.popclosed(node))
        self.mode = self.popmode(node)
        self.border = self.popborder(node)
        self.fill = self.popfill(node)
        self.points = self.poppts(node) #List of strings. Each string contains 3 numbers: 'float, float, section'
        # Private
        self._attribs = ['name','closed','border','fill','mode','points'] # List of all attributes, used for creating an attribute dictionary for output (see output(self))
    # STRING REPRESENTATION
    def __str__(self):
        '''Allows user to use print( <ZContour> ) function'''
        return 'ZContour object:\n-name: '+str(self.name)+'\n-closed: ' \
               +str(self.closed)+'\n-mode: '+str(self.mode) \
               +'\n-border: '+str(self.border)+'\n-fill: '+str(self.fill) \
               +'\n-points: '+str(self.points)+'\n'

# Accessors
    def getpoints(self):
        '''Returns Points attribute (list of strings, each consisting of two numbers \
separated by a single space)'''
        return self.points
    def getxbord(self):
        bord = ''
        for elem in self.border:
            bord += str(elem)+' '
        return str(bord).rstrip()
    def getxfill(self):
        fill = ''
        for elem in self.fill:
            fill += str(elem)+' '
        return str(fill).rstrip()
    def getxpoints(self):
        ret = ''
        for tup in self.points:
            ret += tup+', '
        return ret.rstrip()
    def getattribs(self):
        '''Returns all zcontour attributes'''
        return self.name, self.closed, self.border, self.fill, \
               self.mode, self.points
    def xgetattribs(self):
        '''Returns all zcontour attributes, xml formatting (strings)'''
        return str(self.name), str(self.closed).lower(), self.getxbord(), self.getxfill(), \
            str(self.mode), str(self.getxpoints())
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
        if str(string) == 'None':
            return None
        return str(string).lower() in ('true')
    def popmode(self, node):
        if node.get('mode', None) == None:
            return None
        else:
            return int( node.get('mode') )
    def popborder(self, node):
        '''Populates self.border'''
        bord = [float(elem) for elem in list(node.get('border').split(' '))]
        return bord
    def popfill(self, node):
        '''Populates self.fill'''
        fill = [float(elem) for elem in list(node.get('fill').split(' '))]
        return fill
    def poppts(self, node):
        #partition points into a list of messy crap
        partPoints = list(node.get('points').lstrip(' ').split(','))
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
    def popname(self, node):
        if node == None:
            return None
        return str( node.get('name') )
    def popclosed(self, node):
        if node == None:
            return None
        return node.get('closed')