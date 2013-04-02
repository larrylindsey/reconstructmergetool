import xml.etree.ElementTree as ET
from xmlTree import *
from Series import *
from Section import *


path = '/home/michaelm/Documents/reconstructmergetool/References/testing.xml'
tree = xmlTree(path)
section = Section(tree)

a = ET.Element('Section')
for i in range(len(section)):
    if section[i]._transform != None:
        j = ET.SubElement(a, section[i]._transform._tag)
        b = ET.SubElement(j, section[i]._tag)
    else:
        j = ET.SubElement(a, section[i]._tag)
ET.dump(a)