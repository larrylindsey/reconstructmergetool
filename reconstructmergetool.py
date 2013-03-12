#  Files: reconstructmergetool.py, reconObjects.py
#
#  Description: Driver for reconstructmergetool
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 3/12/2013

from reconObjects import *

path = '/home/michaelm/Documents/reconstructmergetool/testing.xml' #---------
def main():
    # Create list of Transform objects
    transList = TransformList()
    transList.addTfromFile(path)
    print('Created Transform List with '+str(len(transList))+' Transform objects.')
    for i in range( len(transList) ):
        print( transList[i] )
        
    # Create list of Contour objects
    contList = ContourList()
    contList.addCfromFile(path)
    print('Created Contour List with '+str(len(contList))+' Contour objects.')
    for i in range( len(contList) ):
        print( contList[i] )
    
main()
    
