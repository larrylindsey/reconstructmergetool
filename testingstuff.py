import xml.etree.ElementTree as ET
from xmlTree import *
from Series import *
from Section import *
# Qs: are bools case sensitive in Reconstruct?
#     do the spaces matter in points?
#     do the tabs matter in points?

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
for i in range(len(section)): # For every element in a section
    if section[i]._transform != None: # If element has a transform attribute (contour(.xml), image, zcontour)
        #==================================================
        transtag = section[i]._transform._tag 
        attdict = {}
        values = list(section[i].getattribs())
        count = 0
        for att in section[i]._attribs:
            attdict[att] = values[count]
            count += 1
        j = ET.SubElement(a, transtag, attdict) #section[i]._transform.getattribs())
        b = ET.SubElement(j, section[i]._tag)
    else:
        j = ET.SubElement(a, section[i]._tag)




# Print hierarchy
ET.dump(a)