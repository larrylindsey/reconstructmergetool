#  Files: reconstructmergetool.py, Series.py, Section.py, Transform.py,
#         Contour.py, ZContour.py, Image.py, ObjectList.py, xmlTree.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 3/27/2013
#
# Currently working on:
    #===== turn points into list of ints/floats/tuples rather than strings (ZContour)
    #===== transform functions in <Transform>
    #===== Use _tmatrix in <Transform> to change points in Contour object (scimage.transform)
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

# 1) Create a series object
tree1 = xmlTree(path1)
series = Series(tree1)
# 2) Create <section> (Eventually, create multiple <sections> and add to series)
# for <section> in <list_of_sections>:
tree2 = xmlTree(path2)
section = Section(tree2)
# 3) Populate <series> with sections
series.addsection(section)

# ====================================== Test code ======================================
#Currently testing transform stuff on contour/transform objects
print(section._list[1]._transform._dim)
print(section._list[1]._transform._tmatrix)







    
