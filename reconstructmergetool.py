#  Files: reconstructmergetool.py, reconObjects.py, transform.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 3/26/2013

from reconObjects import *
# 1) Create a series object
path1 = '/home/michaelm/Documents/reconstructmergetool/sertesting.ser'
tree1 = xmlTree(path1)
series = Series(tree1)
# 2) Create <section>
path2 = '/home/michaelm/Documents/reconstructmergetool/testing.xml'
tree2 = xmlTree(path2)
section = Section(tree2)
# 3) Populate <series> with sections
series.addsection(section)

##
### Test kosher section creation =======================
##print( section ) # prints info about the section
##print( section._list ) # prints list of items in the section


    
