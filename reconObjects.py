#  Files: reconObjects.py
#
#  Description: Contains the classes used for Reconstruct
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 3/11/2013

import xml.etree.ElementTree as ET

class Transform:
    '''Transform object containing the following data: \n   Dim \n   yCoef \n   xCoef'''

    def __init__(self, dim, ycoef, xcoef):
        self._dim = int(dim)
        self._ycoef = []
        self._xcoef = []
        
        #Add x and y coef attributes to a list
        for char in ycoef:
            if char.isdigit():
                self._ycoef.append( int(char) )
        for char in xcoef:
            if char.isdigit():
                self._xcoef.append( int(char) )        
    def __str__(self):
        return 'Transform object:\nDim: '+str(self.getDim())+'\nYcoef: ' \
               +str(self.getycoef())+'\nXcoef: '+str(self.getxcoef())+'\n'
    
    def getDim(self):
        return self._dim

    def getycoef(self):
        return self._ycoef
    
    def getxcoef(self):
        return self._xcoef

    def getAttribs(self):
        return self.getDim(), self.getycoef(), self.getxcoef()
    
class TransformList:
    '''A list object containing multiple Transform objects.'''
    def __init__(self):
        '''Creates empty TransformList.'''
        self._tList = []
        self._numT = 0

    def __len__(self):
        '''Returns the number of transform objects in the TransformList.'''
        return self._numT

    def __getitem__(self, x):
        if x <= (len(self)-1):
            return self._tList[x]
        else:
            print( 'Invalid argument.')
    
    def isEmpty(self):
        '''Return true if TransformList is empty.'''
        return self._numT == 0
        
    def addT(self, T):
        '''Appends a transform object to the tList.'''
        self._tList.append(T)
        self._numT += 1

    def addTfromFile(self, path):
        '''Parses XML file (path), creates a Transform object, adds the objects to tList.'''
        #parse xml
        tree = ET.parse(path)
        root = tree.getroot() #Section = root.tag, Transform = root, contour = root[x]

        #list of all elements in XML doc
        allList = list( tree.iter() )


        #go through allList, make transform objects, add transform object to tList
        for elem in allList:
            if elem.tag == 'Transform':
                T = Transform(elem.attrib['dim'], elem.attrib['ycoef'], elem.attrib['xcoef'])
                self.addT(T)

