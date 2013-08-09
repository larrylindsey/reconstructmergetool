import sys
import reconstructmergetool as rmt
from Transform import *
from findCalFactor import *
a = sys.argv
def main(a=None):
    if __name__ != '__main__':
        print('reScale')
        return
    path_to_series = sys.argv[1]
    newMag = float(sys.argv[2])
    if len(sys.argv) == 4:
        outpath = sys.argv[3]
    else:
        outpath = str( input('Specify output directory: ') )
    
    ser = rmt.getSeries(path_to_series) # Load series
    reScale(ser, newMag, outpath)

       
def reScale(ser, newMag, outpath):
    
    ser.zeroIdentity()    
    for section in ser.sections:# Set mag field and rescale

        # img objects exist in two locations per section:
        # (1/2): Set newMag for section.imgs[0-x].mag
        oldMag = section.imgs[0].mag
        section.imgs[0].mag = float(newMag)
        scale = newMag/oldMag
#         print('before scale: '+str(section.imgs[0].transform.output())) #===
        tformdImgT = scaleImgTForms(section.imgs[0].transform, scale)
        section.imgs[0].transform = tformdImgT
#         print('after scale, sec.img: '+str(section.imgs[0].transform.output())) #===
        for contour in section.contours:
            # (2/2): Set newMag for contour.img.mag
            if contour.img != None: # if contour is an image contour...
                contour.img = section.imgs[0] #copy section.imgs[0] to contour.img
#                 print('after scale, cont.img: '+str(contour.img.transform.output())) #===
#                 pause = raw_input('your mom') #===
#             else: # if not an image contour...
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
    
    newxCoefs = []
    newyCoefs = []
    if oldT.dim in range(4,7): #Poly. transform
        for newCoefs, oldCoefs in [(newxCoefs, oldT.xcoef), (newyCoefs, oldT.ycoef)]:
            newCoefs.append( oldCoefs[0]*(scale**-1) )
            newCoefs.append( oldCoefs[1] )
            newCoefs.append( oldCoefs[2] )
            newCoefs.append( oldCoefs[3]*scale )
            newCoefs.append( oldCoefs[4]*scale ) #=== scale or 1?
            newCoefs.append( oldCoefs[5]*scale )
            
        newT.xcoef = newxCoefs
        newT.ycoef = newyCoefs
    
    else: # Affine transform
        for newCoefs, oldCoefs in [(newxCoefs, oldT.xcoef), (newyCoefs, oldT.ycoef)]:
            newCoefs.append( oldCoefs[0]*(scale**-1) )
            newCoefs.append( oldCoefs[1] )
            newCoefs.append( oldCoefs[2] )
            newCoefs.append( oldCoefs[3] )
            newCoefs.append( oldCoefs[4] ) #=== scale or 1?
            newCoefs.append( oldCoefs[5] )
        
        newT.xcoef = newxCoefs
        newT.ycoef = newyCoefs
    
    newT.poptform()
    return newT

main(sys.argv)