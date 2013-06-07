import numpy as np
from skimage import transform as tf

class Transform:
    '''Transform object containing the following data: \nTag \nDim \nyCoef \nxCoef \ntmatrix'''
# Python functions
    # INITIALIZE
    def __init__(self, node=None): # node is xml tree node
        '''Initializes the Transform object'''
        # Attributes
        self.tag = 'Transform'
        self.name = 'Transform'
        self.dim = self.popdim(node) #int
        self.ycoef = self.popyxcoef(node)[0]
        self.xcoef = self.popyxcoef(node)[1]
        self.tospace = '' #===
        self.fromspace = '' #===
        # Private
        self._tform = self.poptform()
        self._attribs = ['dim','xcoef','ycoef'] # List of all attributes, used for creating an attribute dictionary for output (see output(self))
    # STRING REPRESENTATION
    def __str__(self):
        '''Allows user to use print( <Transform> ) function'''
        return 'Transform object:\n-dim: '+str(self.dim)+'\n-ycoef: ' \
               +str(self.getycoef())+'\n-xcoef: '+str(self.getxcoef())

# Accessors
    def worldpts(self, points): #=== /usr/local/lib/python2.7/dist-packages/skimage/transform/_geometric.py
        newpts = []
        for pt in points:
            newpts.append( tuple(self._tform.inverse(pt)[0]) )
        return newpts
    def imgpts(self, points): #===
        '''Returns imgpts'''
        return
    def getycoef(self):
        '''Returns ycoefs'''
        ret = ''
        for int in self.ycoef:
            ret += ' '+str(int)
        return ret
    def getxcoef(self):
        '''Returns xcoefs'''
        ret = ''
        for int in self.xcoef:
            ret += ' '+str(int)
        return ret
    def getattribs(self):
        '''Returns Dim, xcoefs, and ycoefs'''
        return self.dim, self.xcoef, self.ycoef
    def xgetattribs(self):
        '''Returns dim, xcoefs, and ycoefs as strings for XML formatting'''
        return str(self.dim), str(self.getxcoef()), str(self.getycoef())
    def output(self):
        '''Returns a dictionary of attributes and a list of contours for building xml'''
        attributes = {}
        keys = self._attribs
        values = list(self.xgetattribs())
        count = 0
        for value in values:
            attributes[keys[count]] = value
            count += 1
        return attributes      
# Mutators              
    def popdim(self, node):
        if node == None:
            return None
        return int(node.get('dim'))  
    def poptform(self):
        '''Creates self._tform variable which represents the transform'''
        if self.xcoef == [] or self.ycoef == [] or self.dim == []:
            print( 'xcoef, ycoef, or dim parameters missing... cannot create tform' )
            return
        a = self.xcoef
        b = self.ycoef
        # Affine transform
        if self.dim in range(0,4):
            if self.dim == 0: 
                tmatrix = np.array( [1,0,0,0,1,0,0,0,1] ).reshape((3,3))
            elif self.dim == 1:
                tmatrix = np.array( [1,0,a[0],0,1,b[0],0,0,1] ).reshape((3,3))
            elif self.dim == 2: # Special case, swap b[1] and b[2] (look at original Reconstruct code: nform.cpp)
                tmatrix = np.array( [a[1],0,a[0],0,b[1],b[0],0,0,1] ).reshape((3,3))
            elif self.dim == 3:
                tmatrix = np.array( [a[1],a[2],a[0],b[1],b[2],b[0],0,0,1]).reshape((3,3))
            return tf.AffineTransform(tmatrix)
        # Polynomial transform
        elif self.dim in range(4,7):
            if self.dim == 4:
                tmatrix = np.array( [a[0],a[1],a[2],a[3],a[4],a[5],b[0],b[1],b[2],b[3],b[4],b[5]] ).reshape((2,6)) # or 6,2? ===
            elif self.dim == 5:
                tmatrix = np.array( [a[0],a[1],a[2],a[3],a[4],a[5],b[0],b[1],b[2],b[3],b[4],b[5]] ).reshape((2,6)) # or 6,2? ===
            elif self.dim == 6:
                tmatrix = np.array( [a[0],a[1],a[2],a[3],a[4],a[5],b[0],b[1],b[2],b[3],b[4],b[5]] ).reshape((2,6)) # or 6,2? ===
            tforward = tf.PolynomialTransform(tmatrix)
            x = np.array(range(0,11))
            y = np.array(range(0,11))
            xx, yy = np.meshgrid(x,y)
            src = np.concatenate( (xx.reshape(1,xx.size),yy.reshape(1,yy.size)) )
            dst = tforward(src)
            treverse = tf.PolynomialTransform()
            treverse.estimate(dst,src,order=2)
            def trevfun(pts): #=== /usr/local/lib/python2.7/dist-packages/skimage/transform/_geometric.py
                return treverse(pts)
            tforward.inverse = trevfun
            return tforward
        else:
            print('Problem with transform.poptform(), check code')
        
    def popyxcoef(self, node):
        '''Populates self.ycoef and self.xcoef'''
        if node == None:
            return [], []
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