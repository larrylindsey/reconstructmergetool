import xml.etree.ElementTree as ET
class xmlTree:
    '''ElementTree containing XML data from <path>'''
    # Python Functions 
    def __init__(self, path):
        self._tag = 'xmltree'
        self._name = str( path.rpartition('/')[2] ) #name = name of xml file
        self._tree = ET.parse(path) #object containing data
        self._treelist = self.gettreelist() #data in _tree stored as a list
    # Accessors
    def gettag(self):
        return self._tag
    def getsection(self):
        '''Returns <section> attributes as a triple (index(int), \
alignLocked(bool), thickness(float).'''
        return int(self._tree.getroot().attrib['index']), \
               float(self._tree.getroot().attrib['thickness']), \
               bool(self._tree.getroot().attrib['alignLocked'])
    def gettreelist(self):
        '''Returns xmlTree as a list object'''
        return list( self._tree.iter() )

    # Mutators
    def chgtag(self, x):
        self._tag = str(x)
    def chgname(self, x):
        self._name = str(x)
    def chgtree(self, x):
        '''Needs to be an ET.parse(<xmlfile>) class.'''
        self._tree = x