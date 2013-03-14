#  Files: reconstructmergetool.py, reconObjects.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 3/14/2013

from reconObjects import *



# create a list of sections?
    # get path to directory containing all the <section>.xml files
        # create list of sections
        # go through each xml file, create tree
path = '/home/michaelm/Documents/reconstructmergetool/testing.xml' #---------
tree = xmlTree(path)
            # create <section>
section = Section(tree)
                # for each <transform (getroot[x]) >, create an image /
                # or contour and add to <section>

currentT = '' #current transform
for node in tree.gettreelist():

    if node.tag == 'Transform':
        currentT = Transform(node)

    elif node.tag == 'Image':
        #create image
        I = Image(node, currentT)
        section._list.addO(I)
       
    elif node.tag == 'Contour':
        #create contour
        C = Contour(node, currentT)
        section._list.addO(C)

print( section )
print( len(section) )



##    # Create list of Transform objects
##    transList = ObjectList()
##    transList.addOfromFile(path, 'transform')
##    print('Created Transform List with '+str(len(transList))+' Transform objects.')
##    for i in range( len(transList) ):
##        print( transList[i] )
##        
##    # Create list of Contour objects
##    contList = ObjectList()
##    contList.addOfromFile(path, 'contour')
##    print('Created Contour List with '+str(len(contList))+' Contour objects.')
##    for i in range( len(contList) ):
##        print( contList[i] )
    
    
