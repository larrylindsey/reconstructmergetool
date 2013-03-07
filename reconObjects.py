#  Files: reconObjects.py
#
#  Description: Contains the classes used for Reconstruct
#
#  Created by: Michael Musslewhite
#
#  Date Created: 3/7/2013
#
#  Date Last Modified: 3/7/2013

import xml.etree.ElementTree as ET

class CompXML:
    '''Object containing a compressed version of xml data to be used /
by other classes and functions. Gathers contour names, points and its /
corresponding transform data (dim, xcoef, ycoef).'''
    def __init_(self, xmlname, path=''): #-------------------------
        self._name = str(xmlname) #name of object is xml file
        self._transList = [] #list of all transform info in the xml
        self._contList = [] #list of all contour info in the xml
        
    
    
class Transform:
    '''Transform object containing dim, xcoef, and ycoef data.'''

    def __init__(self):
        '''Creates empty transform object with default dim = 0 /
        and empty xcoef/ycoef lists.'''
        self._dim = 0
        self._xcoef = []
        self._ycoef = []

    def getAtttributes(self, xml):
        '''Parses xml file dim, xcoef, and ycoef and subsequently /
        adds them to the Transform object.'''
        #create open file object for xml
        #xml = home/michaelm/Documents/reconstructmergetool/testing.xml
    
class Contour:
    def __init__(self):
        self._name = ''
        self._points = []
        







##path = "/home/michaelm/Documents/reconstructmergetool/testing.txt" #TEST---------------
##
##def readTrace(path):
##    '''readTrace() will read from the file located in the path. From \
##        this file, contour points, dim, xcoef, and ycoef will be returned \
##        simultaneously in the form of an array, integer, list and list, \
##        respectively.'''
##    
##    # Create a file object (in read mode)
##    traceFile = open(path, "r")
##    
##    points = []
##    dim = 0
##    xcoef = []
##    ycoef = []
##    
##    for line in traceFile:
##        #Find dim integer
##        if "<Transform dim=" in line:
##            for char in line:
##                if char.isdigit():
##                    dim = int(char)
##
##        #Make xcoef list
##        elif "xcoef=" in line:
##            #Extract only the numbers from the line
##            xcoefnums = line.partition('"')[2].replace('"','').replace('\n','').lstrip(' ')
##            xcoef = xcoefnums.split(' ')
##            print(xcoef)
##
##        #Make ycoef list
##        elif "ycoef=" in line:
##            #Extract only the numbers from the line
##            ycoefnums = line.partition('"')[2].replace('"','').replace('>','').replace('\n','').lstrip(' ')
##            ycoef = ycoefnums.split(' ')
##            print(ycoef)
##
###====================================================================================================
##
##        #Make points array
##        elif "points=" in line:
##            print("points", points) #TEST-------------
##    
##    return points, dim, xcoef, ycoef
##
##readTrace(path) #TEST------------
