import xml.etree.ElementTree as ET
from xmlTree import *
from Series import *
from Section import *

def main():
    path = '/home/michaelm/Documents/reconstructmergetool/References/testing.xml'
    tree = xmlTree(path)
    section = Section(tree)
    strlist = outsection(section)
    output(strlist)

def output(strlist):
     for elem in strlist:
         if '>' not in elem:
             print(elem),
         else:
             print(elem+'\n')
             if '/Transform' in elem:
                 print('\n')
                 
def outsection(section):
    '''Returns a list of strings for xml output of a section'''
    attrib = getattribs(section)
    a = ET.Element('Section', attrib)
    for i in range(len(section)): # For every element in a section
        
        if section[i]._transform != None: # Object has transform
            # Transform xml representation
            attdict = getattribs(section[i]._transform)
            b = ET.SubElement(a, 'Transform', attdict)
            
            # Contour, image, ZContour xml representation
            attdict = getattribs(section[i])
            c = ET.SubElement(b, section[i]._tag, attdict)
        
        else: # Object does not have transform (.ser files)
            attdict = getattribs(section[i])
            j = ET.SubElement(a, section[i]._tag, attdict)
    return ET.tostringlist(a)


def getattribs(object):
    '''Helper function to return a dictionary of attributes'''
    attdict = {}
    values = list( object.getattribs() )
    count = 0
    # Add attribute and value to dictionary
    for key in object._attribs:
        attdict[key] = values[count]
        count += 1
    return attdict

main()
