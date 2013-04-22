class Image:
    '''Image object containing the following attributes: src (string), mag (float), \
contrast (float), brightness (float), red (bool), green (bool), blue (bool), and \
transform (object)'''
# Python functions
    # INITIALIZE
    def __init__(self, node, transform):
        self._tag = 'Image'
        self._name = node.attrib['src']
        self._src = node.attrib['src']
        self._mag = float( node.attrib['mag'] )
        self._cntrst = float( node.attrib['contrast'] )
        self._bright = float( node.attrib['brightness'] )
        self._red = self.popred(node)
        self._green = self.popgreen(node)
        self._blue = self.popblue(node)
        self._transform = transform
        self._attribs = ['mag','contrast','brightness','red','green','blue','src']
    # STRING REPRESENTATION
    def __str__(self):
        '''Allows print( <image> ) function. Returns attributes as string.'''
        return 'Image Object:\n-src: %s\n-mag: %f\n-contrast: %f\n-brightness: %f\n\
-red: %s\n-green: %s\n-blue: %s\n-%s\n'%(self.getattribs())

# Accessors
    def output(self):
        '''Returns a dictionary of attributes and a list of contours for building xml'''
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
        return self._tag
    def getsrc(self):
        '''src ---> string'''
        return self._src
    def getmag(self):
        '''mag ---> float'''
        return self._mag
    def getcontrast(self):
        '''contrast ---> float'''
        return self._cntrst
    def getbrightness(self):
        '''brightness ---> float'''
        return self._bright
    def getred(self):
        '''red ---> bool'''
        return self._red
    def getgreen(self):
        '''green ---> bool'''
        return self._green
    def getblue(self):
        '''blue ---> bool'''
        return self._blue
    def gettransform(self):
        '''transform ---> object'''
        return self._transform
    def xgetattribs(self):
        '''Returns all attributes for <image> (as strings)'''
        return str(self._mag), str(self._cntrst), str(self._bright), \
            str(self._red).lower(), str(self._green).lower(), str(self._blue).lower(), str(self._src)
    def getattribs(self):
        return self._mag, self._cntrst, self._bright, self._red, self._green, self._blue, self._src

# Mutators
    def popred(self, node):
        if node.get('red', None) == None:
            return True
        elif node.attrib['red'].capitalize() == 'True':
            return True
        else:
            return False
    def popgreen(self, node):
        if node.get('green', None) == None:
            return True
        elif node.attrib['green'].capitalize() == 'True':
            return True
        else:
            return False
    def popblue(self, node):
        if node.get('blue', None) == None:
            return True
        elif node.attrib['blue'].capitalize() == 'True':
            return True
        else:
            return False    
    def chgtag(self, x):
        self._tag = str(x)
    def chgsrc(self, x):
        self._src = str(x)  
    def chgmag(self, x):
        self._mag = float(x)
    def chgcontrast(self, x):
        self._cntrst = float(x)
    def chgbrightness(self, x):
        self._bright = float(x)
    def chgred(self, x):
        self._red = bool(x)
    def chggreen(self, x):
        self._green = bool(x)
    def chgblue(self, x):
        self._blue = bool(x)
    def chgtransform(self, x):
        self._transform = x