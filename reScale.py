import sys
import reconstructmergetool as rmt
from findCalFactor import *
print(sys.argv)
# ==== still off by a bit

path_to_series = sys.argv[1]
newMag = float(sys.argv[2])
if len(sys.argv) == 4:
    outpath = sys.argv[3]
else:
    outpath = str( input('Specify output directory: ') )

# Load series
ser = rmt.getSeries(path_to_series)
# Set contours to identity transform
ser.zeroIdentity()
# Set mag field and rescale
for section in ser.sections:
    # img objects exist in two locations per section
    # Set newMag for section.imgs[0-x].mag (1/2)*
    for img in section.imgs:
        oldMag = img.mag
        img.mag = newMag
    scale = newMag/oldMag
    for contour in section.contours:
        # Set newMag for contour.img.mag (2/2)*
        if contour.img != None:
            contour.img.mag = newMag
        else: # if not an image contour, rescale all the points
            pts = contour.points
            newpts = []
            for pt in pts:
                newpts.append( (pt[0]*scale, pt[1]*scale) )
            contour.points = newpts
# Write out series/sections
ser.writeseries(outpath)
ser.writesections(outpath)