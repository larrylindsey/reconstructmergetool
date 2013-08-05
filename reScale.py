import sys
import reconstructmergetool as rmt
from Series import *
from Section import *
from Transform import *
from Image import *
from Contour import *
from ZContour import *
from skimage import transform as tf
import findCalFactor as fcf

 
if len(sys.argv) > 1:
    path_to_series = str( sys.argv[1] )
 
def reScale(path_to_series):
    # get scale
    scale = fcf.findCalFactor(path_to_series)
    
    # create series
    ser = rmt.getSeries(path_to_series)
    ser.zeroIdentity()

reScale(path_to_series)

