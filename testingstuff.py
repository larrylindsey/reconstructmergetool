import xml.etree.ElementTree as ET
from xmlTree import *
from Series import *
from Section import *
# Qs: are bools case sensitive in Reconstruct?
#     do the spaces matter in points?
#     do the tabs matter in points?


# Series


# Section
attrib = {}
values = list(section.getattribs())
count = 0
for key in section._attribs:
    attrib[key] = values[count]
    count += 1

# Contours, Images, Transforms, ZContours
a = ET.Element('Section', attrib)
for i in range(len(section)): # For every element in a section
    
    if section[i]._transform != None: # If element has a transform attribute (contour(.xml), image, zcontour)
        # Create transform subelement
        attdict = {}
        values = list( section[i]._transform.getattribs() )
        count = 0
        for att in section[i]._transform._attribs:
            attdict[att] = values[count]
            count += 1 
        b = ET.SubElement(a, 'Transform', attdict)
        
        # Create subelement (contour, image, zcontour) as transform subelement
        attdict = {}
        values = list( section[i].getattribs() )
        count = 0
        for att in section[i]._attribs:
            attdict[att] = values[count]
            count += 1
        c = ET.SubElement(b, section[i]._tag, attdict)
    
    else:
        j = ET.SubElement(a, section[i]._tag)

strlist = ET.tostringlist(a)
print(strlist)