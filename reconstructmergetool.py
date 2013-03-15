#  Files: reconstructmergetool.py, reconObjects.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 3/15/2013

from reconObjects import *
# 1) Create a series object
#sectionList = ''
#series = Series(sectionList)

# 2) Populate <series> with sections
path = '/home/michaelm/Documents/reconstructmergetool/testing.xml' #=========
tree = xmlTree(path)
section = Section(tree)

# Test kosher section creation =======================
print( section ) # prints info about the section
print( section._list ) # prints list of items in the section


    
    
