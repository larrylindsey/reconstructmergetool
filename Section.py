# from ObjectList import *
from Transform import *
from Image import *
from Contour import *
class Section:
    '''<Section> is an object with attributes: index, thickness, alignLocked \
as well as a list containing <Image> and <Contour> objects. \
Attributes printed with print(<Section>) objects in list printed with print(<Section>._list)'''
# Python Functions
    # INITIALIZE
    def __init__(self, root, name='Unknown'):
        # Create <section>
        self._name = name
        self._tag = 'Section'
        self._list, self._imgs = self.poplists(root) #List of contours, list of images
        self._index = int(root.attrib['index'])
        self._thick = float(root.attrib['thickness'])
        self._alignLock = root.attrib['alignLocked']
        self._attribs = ['index','thickness','alignLocked']
    # LENGTH
    def __len__(self):
        '''Allows use of len(<Section>) function. Returns length'''
        return len(self._list)
    # INDEX REPRESENTATION
    def __getitem__(self,x):
        '''Allows use of <Section>[x] to return xth elements in list'''
        return self._list[x]
    # STRING REPRESENTATION
    def __str__(self):
        '''Allows use of print(<section>) function.'''
        return 'Index: %d\nThickness: %f\nAlign Locked: %s'%(self._index, \
                                                                 self._thick, \
                                                                 self._alignLock)     
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
        '''Return main attributes as strings'''
        return self._index, self._thick, self._alignLock
    def xgetattribs(self):
        return str(self._index), str(self._thick), str(self._alignLock).lower()
# Mutators       
    def poplists(self, root):
        '''Populates section with Contours/Images/etc.'''
        contours = []
        images = []
        for transform in root:
            imgflag = False
            for child in transform:
                if child.tag == 'Image':
                    imgflag = True
                    I = Image(child, Transform(transform))
                    images.append(I)
                elif child.tag == 'Contour':
                    C = Contour(child, imgflag, Transform(transform))
                    contours.append(C)
                    imgflag = False
                elif child.tag == 'ZContour':
                    Z = ZContour(child, Transform(transform))
                    contours.append(Z)
        return contours, images