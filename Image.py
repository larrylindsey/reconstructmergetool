class Image:
    '''Image object containing the following attributes: src (string), mag (float), \
contrast (float), brightness (float), red (bool), green (bool), blue (bool), and \
transform (object)'''
    # Python functions
    def __init__(self, node, transform):
        self._tag = 'Image'
        self._src = node.attrib['src']
        self._mag = float( node.attrib['mag'] )
        self._cntrst = float( node.attrib['contrast'] )
        self._bright = float( node.attrib['brightness'] )
        self._red = bool( node.attrib['red'].capitalize() )
        self._green = bool( node.attrib['green'].capitalize() )
        self._blue = bool( node.attrib['blue'].capitalize() )
        self._trnsfrm = transform
    def __str__(self):
        '''Allows print( <image> ) function. Returns attributes as string.'''
        return 'Image Object:\n-src: %s\n-mag: %f\n-contrast: %f\n-brightness: %f\n\
-red: %s\n-green: %s\n-blue: %s\n-%s\n'%(self.getattribs())

    # Accessors
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
        return self._trnsfrm
    def getattribs(self):
        '''Returns all attributes for <image>'''
        return self.getsrc(), self.getmag(), self.getcontrast(), \
               self.getbrightness(), self.getred(), self.getgreen(), \
               self.getblue(), self.gettransform()

    # Mutators
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
        self._trnsfrm = x