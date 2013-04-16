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
        self._list = self.popseclist(root)
        self._index = int(root.attrib['index'])
        self._thick = float(root.attrib['thickness'])
        self._alignLock = root.attrib['alignLocked']
        self._attribs = ['index','thickness','alignLocked'] # List of attributes for xml output
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
    def getattribs(self):
        '''Return main attributes as strings'''
        return str(self._index), str(self._thick), str(self._alignLock).lower()

# Mutators       
    def popseclist(self, root):
        '''Populates section with Contours/Images/etc.'''
        tmpT = '' #current transform
        ret = []
        for transform in root:
            ret.append(Transform(transform))
            for child in transform:
                if child.tag == 'Image':
                    I = Image(child, tmpT)
                    ret.append(I)
                elif child.tag == 'Contour':
                    C = Contour(child, tmpT)
                    ret.append(C)
                elif child.tag == 'ZContour': #=== can image have ZContour?
                    Z = ZContour(child, tmpT)
                    ret.append(Z)
        return ret 