#  Files: reconObjects.py
#
#  Description: Contains the classes used for reconstructmergetool.py
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 3/12/2013
#
#  Currently implementing:
    #===== Add reference to Transform Object in Contour object
    #===== Add imgpts and worldpts in Contour object
    #===== Group Contours together per section
    #===== Check __getitem__ code in objectlists

import xml.etree.ElementTree as ET

class Transform:
    '''Transform object containing the following data: \n   Dim \n \
  yCoef \n   xCoef'''

    def __init__(self, dim, ycoef, xcoef):
        '''Initializes the Transform object'''
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
        '''Allows user to use print( <Transformobject> )'''
        return 'Transform object:\nDim: '+str(self.getDim())+'\nYcoef: ' \
               +str(self.getycoef())+'\nXcoef: '+str(self.getxcoef())+'\n'
    
    def getDim(self):
        '''Returns Dim'''
        return self._dim

    def getycoef(self):
        '''Returns ycoefs'''
        return self._ycoef
    
    def getxcoef(self):
        '''Returns xcoefs'''
        return self._xcoef

    def getAttribs(self):
        '''Returns Dim, ycoefs, and xcoefs'''
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
        '''Allows the ability to retrieve xth item from the TransformList'''
        if x <= (len(self)-1): #===================== need to double check
            return self._tList[x]
        else:
            print( 'Invalid argument. X is outside of list range.')
    
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

class Contour:
    '''Contour object containing the following data: \n   Name \n \
  Hidden \n   Closed \n   Simplified \n   Border \n   Fill \n \
  Mode \n   Points'''

    def __init__(self, name, hidden, closed, simplified, border, \
                 fill, mode, points):
        '''Initializes the Contour object'''
        #Added from parameters
        self._name = str(name)
        self._hidden = bool(hidden)
        self._closed = bool(closed)
        self._simplified = bool(simplified)
        self._mode = int(mode)

        #Analyze parameters, then add
        self._border = []
        self._fill = []
        self._points = points
            #border
        for char in border:
            if char.isdigit():
                self._border.append( int(char) )
            #fill
        for char in fill:
            if char.isdigit():
                self._fill.append( int(char) )

    def __str__(self):
        '''Allows user to use print( <Contourobject> )'''
        return 'Contour object:\nName: '+str(self.getName())+'\nHidden: ' \
               +str(self.getHidden())+'\nClosed: '+str(self.getClosed()) \
               +'\nSimplified: '+str(self.getSimp())+'\nMode: '+str(self.getMode()) \
               +'\nBorder: '+str(self.getBord())+'\nFill: '+str(self.getFill()) \
               +'\nPoints: '+str(self.getPoints())+'\n'
    
    def getName(self):
        '''Returns Name attribute'''
        return self._name

    def getHidden(self):
        '''Returns Hidden attribute'''
        return self._hidden

    def getClosed(self):
        '''Returns Closed attribute'''
        return self._closed
    
    def getSimp(self):
        '''Returns Simplified attribute'''
        return self._simplified
    
    def getMode(self):
        '''Returns Mode attribute'''
        return self._mode
    
    def getBord(self):
        '''Returns Border attribute'''
        return self._border
    
    def getFill(self):
        '''Returns Fill attribute'''
        return self._fill
    
    def getPoints(self):
        '''Returns Points attribute'''
        return self._points
    
    def getAttribs(self):
        '''Returns Dim, ycoefs, and xcoefs'''
        return self.getName(), self.getHidden(), self.getClosed(), self.getSimp(), \
               self.getMode(), self.getBord(), self.getFill(), self.getPoints

class ContourList:
    '''A list object containing multiple Contour objects.'''
    def __init__(self):
        '''Creates empty ContourList.'''
        self._cList = []
        self._numC = 0

    def __len__(self):
        '''Returns the number of Contour objects in the ContourList.'''
        return self._numC

    def __getitem__(self, x):
        '''Allows the ability to retrieve xth item from the ContourList'''
        if x <= (len(self)-1): #===================== need to double check
            return self._cList[x]
        else:
            print( 'Invalid argument. X is outside of list range.')
    
    def isEmpty(self):
        '''Return true if ContourList is empty.'''
        return self._numC == 0
        
    def addC(self, C):
        '''Appends a contour object to the cList.'''
        self._cList.append(C)
        self._numC += 1

    def addCfromFile(self, path):
        '''Parses XML file (path), creates a Contour object, adds the objects to cList.'''
        #parse xml
        tree = ET.parse(path)
        root = tree.getroot()

        #list of all elements in XML doc
        allList = list( tree.iter() )

        #go through allList, make contour objects, add contour object to cList
        for elem in allList:
            if elem.tag == 'Contour':
                #partition points into a list of messy crap
                partPoints = list(elem.attrib['points'].lstrip(' ').split(','))

                #make a new list of clean points, to be added to object
                ptList = []
                for i in range( len(partPoints) ):
                    ptList.append( partPoints[i].strip() )
                #remove empty points
                for i in range( len(ptList) ):
                    if ptList[i] == '':
                        ptList.remove('')
                
                C = Contour(elem.attrib['name'], elem.attrib['hidden'], elem.attrib['closed'], \
                            elem.attrib['simplified'], elem.attrib['border'], elem.attrib['fill'], \
                            elem.attrib['mode'], ptList)
                self.addC(C)
