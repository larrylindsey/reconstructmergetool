import sys
import reconstructmergetool as rmt
from Transform import *
from findCalFactor import *

path_to_series = sys.argv[1]
newMag = float(sys.argv[2])
if len(sys.argv) == 4:
    outpath = sys.argv[3]
else:
    outpath = str( input('Specify output directory: ') )

ser = rmt.getSeries(path_to_series) # Load series
    
def main(ser, newMag, outpath):
    ser.zeroIdentity()    
    for section in ser.sections:# Set mag field and rescale

        # img objects exist in two locations per section:
        # (1/2): Set newMag for section.imgs[0-x].mag
        for img in section.imgs:
            oldMag = float(img.mag)
            print(img.transform.output()) #===
            pause = raw_input('freeze') #===
            img.mag = float(newMag)
            scale = float(newMag)/float(oldMag) #=== moved into loop instead of out+after
            img.transform = scaleImgTForms(img.transform, scale) #===
        
        for contour in section.contours:
            # (2/2): Set newMag for contour.img.mag
            if contour.img != None: # if contour is an image contour...
                print(contour.img.transform.output()) #===
                pause = raw_input('freeze') #===
                contour.img.mag = float(newMag) #...apply new mag field
                contour.img.transform = scaleImgTForms(contour.img.transform, scale) #===
            else: # if not an image contour...
                #...rescale all the points
                pts = contour.points
                newpts = []
                for pt in pts:
                    newpts.append( (pt[0]*scale, pt[1]*scale) )
                contour.points = newpts
    # Write out series/sections
    ser.writeseries(outpath)
    ser.writesections(outpath)

def scaleImgTForms(oldT, scale):
    newT = Transform()
    newT.dim = oldT.dim
    if oldT.dim in range(4,7): #Poly. transform
        newxCoefs = []
        newxCoefs.append( oldT.xcoef[0]*(scale**-1) )
        newxCoefs.append( oldT.xcoef[1] )
        newxCoefs.append( oldT.xcoef[2] )
        newxCoefs.append( oldT.xcoef[3]*scale )
        newxCoefs.append( oldT.xcoef[4]*scale ) #=== scale or 1?
        newxCoefs.append( oldT.xcoef[5]*scale )
        newyCoefs = []
        newyCoefs.append( oldT.ycoef[0]*(scale**-1) )
        newyCoefs.append( oldT.ycoef[1] )
        newyCoefs.append( oldT.ycoef[2] )
        newyCoefs.append( oldT.ycoef[3]*scale )
        newyCoefs.append( oldT.ycoef[4]*scale ) #=== scale or 1?
        newyCoefs.append( oldT.ycoef[5]*scale )
        
        newT.xcoef = newxCoefs
        newT.ycoef = newyCoefs
    
    else: # Affine transform
        newxCoefs = []
        newxCoefs.append( oldT.xcoef[0]*(scale**-1) )
        newxCoefs.append( oldT.xcoef[1] )
        newxCoefs.append( oldT.xcoef[2] )
        newxCoefs.append( oldT.xcoef[3] )
        newxCoefs.append( oldT.xcoef[4] )
        newxCoefs.append( oldT.xcoef[5] )
        newyCoefs = []
        newyCoefs.append( oldT.ycoef[0]*(scale**-1) )
        newyCoefs.append( oldT.ycoef[1] )
        newyCoefs.append( oldT.ycoef[2] )
        newyCoefs.append( oldT.ycoef[3] )
        newyCoefs.append( oldT.ycoef[4] )
        newyCoefs.append( oldT.ycoef[5] )
        
        newT.xcoef = newxCoefs
        newT.ycoef = newyCoefs
    
    newT.poptform()
    return newT

main(ser, newMag, outpath)