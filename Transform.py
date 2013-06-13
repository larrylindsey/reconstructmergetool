import numpy as np
from skimage import transform as tf
import math

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
    def worldpts(self, points):
        '''Returns worldpts'''
        newpts = self._tform.inverse(np.asarray(points))
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
                tmatrix = np.array( [a[1],a[2],a[0],b[1],b[2],b[0],0,0,1] ).reshape((3,3))
            return tf.AffineTransform(tmatrix)
        # Polynomial transform
        elif self.dim in range(4,7):
            tmatrix = np.array( [a[0],a[1],a[2],a[3],a[4],a[5],b[0],b[1],b[2],b[3],b[4],b[5]] ).reshape((2,6))
            # create matrix of coefficients 
            tforward = tf.PolynomialTransform(tmatrix)
            
            def getrevt(pts): # pts are a np.array
                tfpts = tforward(pts) # nparray of pts after forward transform
                newpts = [] # list of final estimates of (x,y)
                for i in range( len(tfpts) ):
                    # (u,v) for which we want (x,y)
                    u, v = pts[i,0], pts[i,1]
#                     print('Current pt: '+str(u)+','+str(v))
                    # initial guess of (x,y)
                    x0, y0 = 0.0, 0.0
                    # get forward tform of initial guess
                    u0, v0 = tforward(np.asarray([(x0,y0)]))[:,0][0],tforward(np.asarray([(x0,y0)]))[:,1][0]
                    for i in range(10):
                        e = 1.0 # reduce error to this limit 
                        epsilon = 5e-10
                        while e > epsilon and i<10:
                            i+=1
                            # compute Jacobian
                            l = a[1] + a[3]*y0 + 2.0*a[4]*x0
                            m = a[2] + a[3]*x0 + 2.0*a[5]*y0
                            n = b[1] + b[3]*y0 + 2.0*b[4]*x0
                            o = b[2] + b[3]*x0 + 2.0*b[5]*y0
                            p = l*o - m*n # determinant for inverse
                            if math.fabs(p) > epsilon:
                                # increment x0,y0 by inverse of Jacobian
                                x0 = x0 + ((o*(u-u0) - m*(v-v0))/p)
                                y0 = y0 + ((l*(v-v0) - n*(u-u0))/p)
                            else:
                                # try Jacobian transpose instead
                                x0 = x0 + (l*(u-u0) + n*(v-v0))        
                                y0 = y0 + (m*(u-u0) + o*(v-v0))
                            # get forward tform of current guess            
                            u0, v0 = tforward(np.asarray([(x0,y0)]))[:,0][0],tforward(np.asarray([(x0,y0)]))[:,1][0]
                            # compute closeness to goal
                            e = math.fabs(u-u0) + math.fabs(v-v0)
                    # append final estimate of (x,y) to newpts list
                    newpts.append((x0,y0))     
                newpts = np.asarray(newpts)    
#                 print('Newpts:\n'+str(newpts))               
                return newpts
            tforward.inverse = getrevt
            # ============ DEBUG HERE
            testarr = np.asarray([(0, 0), (4096, 0), (4096, 4096), (0, 4096)])
            print('ptarray:\n'+str(testarr))
            print('tf(tfinvers(pts)):\n'+str(tforward(tforward.inverse( testarr ))))
            print('tfinvers(tf(pts)):\n'+str(tforward.inverse(tforward( testarr ))))
            quit()
            
            return tforward
            
        
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