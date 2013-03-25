#  Files: reconstructmergetool.py, reconObjects.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 3/25/2013

from reconObjects import *
# 1) Create a series object
path = '/home/michaelm/Documents/reconstructmergetool/sertesting.ser'
tree = xmlTree(path)
series = Series(tree)
# 2) Create <section>
path = '/home/michaelm/Documents/reconstructmergetool/testing.xml'
tree = xmlTree(path)
section = Section(tree)
# 3) Populate <series> with sections
series.addsection(section)

##
### Test kosher section creation =======================
##print( section ) # prints info about the section
##print( section._list ) # prints list of items in the section


    
    
