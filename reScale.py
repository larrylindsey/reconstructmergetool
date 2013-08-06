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
 
def reScale(path_to_series, name=None, outpath=None):
    # get scale
    scale = fcf.findCalFactor(path_to_series)
    
    # create series w/ sections, etc.
    ser = rmt.getSeries(path_to_series)
    # perform forward tform to identity transform
    ser.zeroIdentity()
    
    # scale traces
    for section in ser.sections:
        # rescale contour points
        for contour in section:
            newPts = []
            # create list of scaled points for this contour
            for pt in contour.points:
                newPts.append( (pt[0]*scale,pt[1]*scale) )
            contour.points = newPts
        #replace mag factor === to what? 0.0022?
#         section.imgs[0].mag = 
    # output new series
    if outpath == None:
        outpath = str(input('Enter path to output folder: '))
    ser.writeseries(outpath)
    ser.writesections(outpath)
reScale(path_to_series)


