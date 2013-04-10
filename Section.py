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
    def __init__(self, xmlTree):
        # Create <section>
        self._name = xmlTree._name
        self._list = self.popseclist(xmlTree)
        self._tag = 'Section'
        # Create <section> attributes
        self._index = xmlTree.getsection()[0]
        self._thick = xmlTree.getsection()[1]
        self._alignLock = xmlTree.getsection()[2]
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
    def gettag(self):
        '''--> (str)'''
        return str(self._tag)
    def getindex(self):
        '''--> (int)'''
        return int(self._index)
    def getthickness(self):
        '''--> (float)'''
        return float(self._thick)
    def getalignlock(self):
        '''--> (bool)''' 
        return bool(self._alignLock)
    def getattribs(self):
        '''Return main attributes as strings'''
        return str(self.getindex()), str(self.getthickness()), str(self.getalignlock()).lower()

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
    def popseclist(self,xmlTree):
        '''Populates section with Contours/Images/etc.'''
        tmpT = '' #current transform
        ret = []
        for node in xmlTree.gettreelist():
            if node.tag == 'Transform':
                tmpT = Transform(node)
            elif node.tag == 'Image':
                I = Image(node, tmpT)
                ret.append(I)
            elif node.tag == 'Contour':
                C = Contour(node, tmpT)
                ret.append(C)
            elif node.tag == 'ZContour': #=== can image have ZContour?
                Z = ZContour(node, tmpT)
                ret.append(Z)
        return ret 