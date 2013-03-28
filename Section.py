from ObjectList import *
from Transform import *
from Image import *
from Contour import *
class Section:
    '''<Section> is an object with attributes: index, thickness, alignLocked \
as well as a list containing <Image> and <Contour> objects. \
Attributes printed with print(<Section>) objects in list printed with print(<Section>._list)'''
# Python Functions
    # INITIALIZE
    def __init__(self, xmlTree):
        # Create <section>
        self._name = xmlTree._name
        self._list = ObjectList()
        self._tag = 'Section'
        # Create <section> attributes
        self._index = xmlTree.getsection()[0]
        self._thick = xmlTree.getsection()[1]
        self._alignLock = xmlTree.getsection()[2]
        # Populate section with image, contour and transforms
        tmpT = '' #current transform
        for node in xmlTree.gettreelist():
            if node.tag == 'Transform':
                tmpT = Transform(node)
            elif node.tag == 'Image':
                I = Image(node, tmpT)
                self._list.addO(I)
            elif node.tag == 'Contour':
                C = Contour(node, tmpT)
                self._list.addO(C)
            elif node.tag == 'ZContour':
                Z = ZContour(node, tmpT)
                self._list.addO(Z)
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
    def gettag(self):
        '''--> (str)'''
        return self._tag
    def getindex(self):
        '''--> (int)'''
        return self._index
    def getthickness(self):
        '''--> (float)'''
        return self._thick
    def getalignlock(self):
        '''--> (bool)''' 
        return self._alignLock

# Mutators
    def chgtag(self, x):
        self._tag = str(x)
    def chgindex(self, x):
        self._index = int(x)
    def chgthickness(self, x):
        self._thick = float(x)
    def chgalignlock(self, x):
        self._alignLock = bool(x)
    def chgtag(self, x):
        self._tag = str(x)