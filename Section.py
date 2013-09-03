from Transform import *
from Image import *
from Contour import *
from ZContour import *
class Section:
# Python Functions
    # INITIALIZE
    def __init__(self, root=None, name='Unknown'): #root is xml tree
        # Create <section>
        self.name = name
        self.tag = 'Section'
        # Contours/Images
        self.contours = self.poplists(root)[0] # List of contours 
        self.imgs = self.poplists(root)[1] # list of images
        # Attributes
        self.index = self.popindex(root) #int
        self.thickness = self.popthickness(root) #float
        self.alignLocked = self.popalignLocked(root)
        # Private
        self._attribs = ['index','thickness','alignLocked'] # List of all attributes, used for creating an attribute dictionary for output (see output(self))
    # LENGTH
    def __len__(self):
        '''Allows use of len(<Section>) function. Returns length of contours'''
        return len(self.contours)
    # allows indexing of Section object
    def __getitem__(self,x):
        '''Allows use of <Section>[x] to return xth elements in list'''
        return self.contours[x]
    # print(<Section>) output
    def __str__(self):
        '''Allows use of print(<section>) function.'''
        return 'Index: %d\nThickness: %f\nAlign Locked: %s'%(self.index, \
                                                                 self.thickness, \
                                                                 self.alignLocked)   
    def __eq__(self, other):
        '''Allows use of == between multiple objects'''
        return self.output() == other.output()
    def __ne__(self, other):
        '''Allows use of != between multiple objects'''
        return self.output() != other.output() 
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
    def getattribs(self):
        '''Returns attributes'''
        return self.index, self.thickness, self.alignLocked
    def xgetattribs(self):
        '''Returns attributes in xml output format'''
        return str(self.index), str(self.thickness), str(self.alignLocked).lower()
# Mutators
    def s2b(self, string):
        '''Converts string to bool'''
        if string == 'None':
            return None
        else:
            return string.lower() in ('true')       
    def poplists(self, root):
        '''Populates section object with Contours/Images/etc.'''
        contours = []
        images = []
        if root == None:
            return contours, images
        for transform in root:
            imgflag = None
            for child in transform:
                if child.tag == 'Image':
                    imgflag = True
                    I = Image(child, Transform(transform))
                    images.append(I)
                elif child.tag == 'Contour':
                    C = Contour(child, imgflag, Transform(transform))
                    if imgflag: #===
                        C.img = I
                    contours.append(C)
                    imgflag = None
                elif child.tag == 'ZContour': # No ZContours in Sections?
                    raw_input('ZCont in section') #=== testing ^ question
                    Z = ZContour(child, Transform(transform))
                    contours.append(Z)
        #=== Check for multiple images; still need to match domain1 contour and image transforms (imageOverride issue only?)
        if len(images) > 1:
            srcList = set([img.src for img in images])
            if len(srcList) == 1:
                images = [images[0]]
            else: #===
                print('Multiple image sources present in '+self.name)
            domain1 = [cont for cont in contours if cont.name == 'domain1'][0]
            if images[0].transform.output() != domain1.transform.output():
                raw_input('Image transform does not match domain1 transform for '+self.name)
        return contours, images
    def popindex(self, root):
        if root == None:
            return None
        return int(root.get('index'))
    def popthickness(self, root):
        if root == None:
            return None
        return float(root.get('thickness'))
    def popalignLocked(self, root):
        if root == None:
            return None
        return root.get('alignLocked')
            