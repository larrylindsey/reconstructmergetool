import xml.etree.ElementTree as ET
from xmlTree import *
from Series import *
from Section import *


path = '/home/michaelm/Documents/reconstructmergetool/References/testing.xml'
tree = xmlTree(path)
section = Section(tree)
# Series

# Section
attrib = {}
values = list(section.getattribs())
count = 0
for key in section._attribs:
    attrib[key] = values[count]
    count += 1
print(attrib)

# Contours, Images, Transforms, ZContours
a = ET.Element('Section', attrib)
for i in range(len(section)):
    if section[i]._transform != None:
        j = ET.SubElement(a, section[i]._transform._tag, {'hi':'40','lo':'4'}) #section[i]._transform.getattribs())
        b = ET.SubElement(j, section[i]._tag)
    else:
        j = ET.SubElement(a, section[i]._tag)




# Print hierarchy
ET.dump(a)