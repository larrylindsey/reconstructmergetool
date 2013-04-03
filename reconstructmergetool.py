#  Files: reconstructmergetool.py, Series.py, Section.py, Transform.py,
#         Contour.py, ZContour.py, Image.py, ObjectList.py, xmlTree.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 4/3/2013
#
# Currently working on:
    #===== XML file creation (testingstuff.py)
        # Problems: Outputting transform for every object rather than mult. objects within a single transform
        #           Output lists, tuples in correct format (e.g. points, etc.)
        # 1) read in section, write out section
        # 2) read in section, write out section with all dim = 0
        # 3) check if read similarly in reconstruct
    #===== ZContour: turn points into list of ints/floats/tuples rather than strings
    #===== Check comments/docstrings
from xmlTree import *
from Series import *
from Section import *

# Series file (testing)
path1 = '/home/michaelm/Documents/reconstructmergetool/References/sertesting.ser'
# Section file (testing)
path2 = '/home/michaelm/Documents/reconstructmergetool/References/testing.xml'
# Contour/Transform object (testing)
path3 = '/home/michaelm/Documents/reconstructmergetool/References/transformtesting.xml'
# Path to write .xml
outPath = '/home/michaelm/Documents/reconstructmergetool/References/outSection.xml'

# 1) Create a series object
tree1 = xmlTree(path1)
series = Series(tree1)
# 2) Create <section> (Eventually, create multiple <sections> and add to series)
# for <section> in <list_of_sections>:
tree2 = xmlTree(path2)
section = Section(tree2)
# 3) Populate <series> with sections
series.addsection(section)

# 4) Test transforms
# tree3 = xmlTree(path3)
# section = Section(tree3)
# print(section._list)
# for i in range(len(section)):
#     print section[i]
# 
contour = section[1]
print(contour.gettracepts())
print(contour.getworldpts())
# 
contour = section[2]
print(contour.gettracepts())
print(contour.getworldpts())

print(series.getattribs())
    
