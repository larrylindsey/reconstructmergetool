import xml.etree.ElementTree as ET
  
def output(strlist, outpath, type='xml', mode='w'):
    '''Depending on input type (default = 'xml'), writes an appropriate document in outpath. \
    type = 'xml' writes to .xml file \
    type = 'ser' writes to .ser file \
    type = anything else wrties to console'''
    print(strlist)
    if type == 'xml': #Write to xml file
        f = open(outpath,mode)
        # XML header
        f.write('<?xml version="1.0"?>\n')
        f.write('<!DOCTYPE Section SYSTEM "section.dtd">\n\n')
        
        # Flags for keeping Contour after Image within same Transform
        ignore = False
        ignore2 = False 
        
        for elem in strlist: #===
            # Image has contour object within same transform.
            # Therefore, don't print the </Transform> or the
            # <Transform> with associated Contour
            
            if '<Image' in elem:
                ignore = True #Check for '<Transform' and ignore all attributes 
                f.write(elem),

            elif ignore:
                if '<Transform' in elem: #Ignore everything until next Contour
                    ignore2 = True

                elif '<Contour' in elem: # Turn flag off once next Contour reached
                    f.write(elem),
                    ignore = False
                    ignore2 = False

                elif '>' in elem and not ignore2: # If end of element, new line           
                    elem = elem+'\n'
                    if 'Transform' not in elem:
                        f.write(elem)

                elif not ignore2: #keep on same line
                    f.write(elem),

            
            
            elif '>' in elem and not ignore2: # If end of element, new line           
                elem = elem+'\n'
                f.write(elem)
                if '/Transform' in elem:
                    f.write('\n')
      
            else: #keep on same line
                f.write(elem),

    elif type == 'ser':
        f = open(outpath, mode)
        f.write('<?xml version="1.0"?>\n')
        f.write('<!DOCTYPE Section SYSTEM "series.dtd">\n\n')
        for elem in strlist:
            if '>' not in elem:
                f.write(elem),
            else:
                elem = elem+'\n'
                f.write(elem)
                if '/' in elem:
                    f.write('\n')
    else: #Print to console
        for elem in strlist:
            if '>' not in elem:
                print(elem),
            else:
                print(elem+'\n')
                if '/Transform' in elem:
                    print('\n')
                     
def outseries(series):
    attrib = getattribs(series)
    a = ET.Element('Series', attrib)
    for i in range(len(series._contours)): #Contours/ZContours
        attdict = getattribs(series._contours[i])
        b = ET.SubElement(a, series._contours[i]._tag, attdict)
    return ET.tostringlist(a)
                      
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
            
    return ET.tostringlist(a)


def getattribs(object): #===
    '''Helper function to return a dictionary of attributes'''
    attdict = {}
    values = list( object.getattribs() ) #===
    count = 0
    # Add attribute and value to dictionary
    for key in object._attribs:
#         print(key, values[count])
        attdict[key] = values[count]
        count += 1
    return attdict

