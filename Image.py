class Image:
    '''Image object containing the following attributes: src (string), mag (float), \
contrast (float), brightness (float), red (bool), green (bool), blue (bool), and \
transform (object)'''
# Python functions
    # INITIALIZE
    def __init__(self, node, transform):
        self.tag = 'Image'
        self.name = node.attrib['src']
        self.src = node.attrib['src']
        self.mag = float( node.attrib['mag'] )
        self.contrast = float( node.attrib['contrast'] )
        self.brightness = float( node.attrib['brightness'] )
        self.red = self.popred(node)
        self.green = self.popgreen(node)
        self.blue = self.popblue(node)
        self.transform = transform
        # Private
        self._attribs = ['mag','contrast','brightness','red','green','blue','src'] # List of all attributes, used for creating an attribute dictionary for output (see output(self))
    # print(<Image>) function output
    def __str__(self):
        '''Allows print( <image> ) function. Returns attributes as string.'''
        return '\nImage Object:\n-src: %s\n-mag: %f\n-contrast: %f\n-brightness: %f\n\
-red: %s\n-green: %s\n-blue: %s'%(self.getattribs())

# Accessors
    def output(self):
        '''Returns a dictionary of attributes'''
        attributes = {}
        keys = self._attribs
        values = list(self.xgetattribs())
        count = 0
        for value in values:
            attributes[keys[count]] = value
            count += 1
        return attributes      
    def gettag(self):
        '''tag ---> string'''
        return self.tag
    def getsrc(self):
        '''src ---> string'''
        return self.src
    def getmag(self):
        '''mag ---> float'''
        return self.mag
    def getcontrast(self):
        '''contrast ---> float'''
        return self.contrast
    def getbrightness(self):
        '''brightness ---> float'''
        return self.brightness
    def getred(self):
        '''red ---> bool'''
        return self.red
    def getgreen(self):
        '''green ---> bool'''
        return self.green
    def getblue(self):
        '''blue ---> bool'''
        return self.blue
    def gettransform(self):
        '''transform ---> object'''
        return self.transform
    def xgetattribs(self):
        '''Returns all attributes for <image> (as strings)'''
        return str(self.mag), str(self.contrast), str(self.brightness), \
            str(self.red).lower(), str(self.green).lower(), str(self.blue).lower(), str(self.src)
    def getattribs(self):
        return self.mag, self.contrast, self.brightness, self.red, self.green, self.blue, self.src

# Mutators
    def popred(self, node):
        '''Searches xml node for red attribute'''
        if node.get('red', None) == None:
            return True
        elif node.attrib['red'].capitalize() == 'True':
            return True
        else:
            return False
    def popgreen(self, node):
        '''Searches xml node for green attribute'''
        if node.get('green', None) == None:
            return True
        elif node.attrib['green'].capitalize() == 'True':
            return True
        else:
            return False
    def popblue(self, node):
        '''Searches xml node for blue attribute'''
        if node.get('blue', None) == None:
            return True
        elif node.attrib['blue'].capitalize() == 'True':
            return True
        else:
            return False