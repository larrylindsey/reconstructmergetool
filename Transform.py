import numpy as np
from skimage import transform as tf

class Transform:
    '''Transform object containing the following data: \nTag \nDim \nyCoef \nxCoef \ntmatrix'''
# Python functions
    # INITIALIZE
    def __init__(self, node):
        '''Initializes the Transform object'''
        # Attributes
        self._tag = 'Transform'
        self._dim = int(node.attrib['dim'])
        self._ycoef = self.popyxcoef(node)[0]
        self._xcoef = self.popyxcoef(node)[1]
        self._tform = self.poptform()
        self._attribs = ['dim','xcoef','ycoef']
    # STRING REPRESENTATION
    def __str__(self):
        '''Allows user to use print( <Transform> ) function'''
        return 'Transform object:\n-dim: '+str(self.getdim())+'\n-ycoef: ' \
               +str(self.getycoef())+'\n-xcoef: '+str(self.getxcoef())

# Accessors
    def worldpts(self, points):
        '''Returns worldpts'''
        newpts = []
        for ptset in points:
            newpts.append( tuple(self._tform(list(ptset))[0]) )
        return newpts
    def imgpts(self, points):
        '''Returns imgpts'''
        return
    def gettag(self):
        '''Returns tag (string)'''
        return self._tag
    def getdim(self):
        '''Returns Dim (int)'''
        return self._dim
    def getycoef(self):
        '''Returns ycoefs'''
        ret = ''
        for int in self._ycoef:
            ret += ' '+str(int)
        return ret
    def getxcoef(self):
        '''Returns xcoefs'''
        ret = ''
        for int in self._xcoef:
            ret += ' '+str(int)
        return ret
    def getattribs(self):
        '''Returns Dim, ycoefs, and xcoefs (as string) XML OUTPUT FORMATTING'''
        return str(self.getdim()), str(self.getxcoef()), str(self.getycoef())

# Mutators                
    def chgtag(self, x):
        self._tag = str(x)
    def chgdim(self, x):
        self._dim = int(x)
    def chgycoef(self, x):
        self._ycoef = list(x)
    def chgxcoef(self, x):
        self._xcoef = list(x)
    def poptform(self):
        '''Creates self._tform variable which represents the transform'''
        a = self._xcoef
        b = self._ycoef
        # Affine transform
        if self._dim == 0:
            tmatrix = np.array([1, 0, 0, 0, 1, 0, 0, 0, 1]).reshape((3,3))
        elif self._dim == 1:
            tmatrix = np.array([1, 0, a[0], 0, 1, b[0], 0, 0, 1]).reshape((3,3))
        elif self._dim == 2: # Special case, swap b[1] and b[2]
            tmatrix = np.array([a[1], 0, a[0], 0, b[1], b[0], 0, 0, 1]).reshape((3,3))
        elif self._dim == 3:
            tmatrix = np.array([a[1], a[2], a[0], b[1], b[2], b[0], 0, 0, 1]).reshape((3,3))
        # Polynomial transform
#         elif self._dim == 4:
#         elif self._dim == 5:
#         elif self._dim == 6:
        return tf.AffineTransform(tmatrix)
    def popyxcoef(self, node):
        '''Populates self._ycoef and self._xcoef'''
        # digits added as int, everything else float
        y = []
        for elem in node.attrib['ycoef'].split(' '):
            if elem.isdigit():
                y.append( int(elem) )
            elif elem != '':
                y.append( float(elem) )
        x = []
        for elem in node.attrib['xcoef'].split(' '):
            if elem.isdigit(): 
                x.append( int(elem) )
            elif elem != '':
                x.append( float(elem) )
        return y,x