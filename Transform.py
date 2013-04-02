import numpy as np

class Transform:
    '''Transform object containing the following data: \nTag \nDim \nyCoef \nxCoef \ntmatrix'''
# Python functions
    # INITIALIZE
    def __init__(self, node):
        '''Initializes the Transform object'''
        # Attributes
        self._tag = 'Transform'
        self._dim = int(node.attrib['dim'])
        self._ycoef = []
        self._xcoef = []
        self._tmatrix = []
        # Populate list attributes
        self.popyxcoef(node)
        self.poptmat()
    # STRING REPRESENTATION
    def __str__(self):
        '''Allows user to use print( <Transform> ) function'''
        return 'Transform object:\n-dim: '+str(self.getdim())+'\n-ycoef: ' \
               +str(self.getycoef())+'\n-xcoef: '+str(self.getxcoef()) \
               +'\n-tmatrix: '+str(self._tmatrix)

# Accessors
    def gettag(self):
        '''Returns tag (string)'''
        return self._tag
    def getdim(self):
        '''Returns Dim (int)'''
        return self._dim
    def getycoef(self):
        '''Returns ycoefs'''
        return self._ycoef
    def getxcoef(self):
        '''Returns xcoefs'''
        return self._xcoef
    def getattribs(self):
        '''Returns Dim, ycoefs, and xcoefs'''
        return self.getDim(), self.getycoef(), self.getxcoef()

# Mutators
    def popyxcoef(self, node):
        '''Populates self._ycoef and self._xcoef'''
        # digits added as int, everything else float
        for elem in node.attrib['ycoef'].split(' '):
            if elem.isdigit():
                self._ycoef.append( int(elem) )
            elif elem != '':
                self._ycoef.append( float(elem) )
        for elem in node.attrib['xcoef'].split(' '):
            if elem.isdigit(): 
                self._xcoef.append( int(elem) )
            elif elem != '':
                self._xcoef.append( float(elem) )
    def poptmat(self):
        '''Populates self._tmatrix'''
        a = self._xcoef
        b = self._ycoef
        if self._dim in range(0,4): # Dim: 0-3; Affine ============
            self._tmatrix = np.array([a[1], a[2], a[0], b[1], b[2], b[0], 0, 0, 1]).reshape((3,3))
        #elif self._dim in range(4,7): # Dim: 4-6; Polynomial ============
         #   self._tmatrix = np.[]
    def chgtag(self, x):
        self._tag = str(x)
    def chgdim(self, x):
        self._dim = int(x)
    def chgycoef(self, x):
        self._ycoef = list(x)
    def chgxcoef(self, x):
        self._xcoef = list(x)