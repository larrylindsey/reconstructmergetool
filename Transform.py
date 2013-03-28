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