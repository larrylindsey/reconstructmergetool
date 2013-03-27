class ObjectList:
    '''A list object containing multiple objects.'''
    # Python functions
    def __init__(self):
        '''Creates empty ObjectList.'''
        self._tag = 'ObjectList'
        self._list = []
        self._len = 0
    def __len__(self):
        '''Allows use of len( <ObjectList> ) function. \
Returns the number of objects in the ObjectList.'''
        return self._len
    def __getitem__(self, x):
        '''Allows the use of <ObjectList>[x] function. \
Returns xth item from the ObjectList'''
        if x <= (len(self)-1):
            return self._list[x]
    def __str__(self):
        '''Allows use of print( <ObjectList> ) function.'''
        taglist = []
        for i in range(len(self)):
            taglist.append( self._list[i].gettag() )
        return str(taglist)
    
    # Accessors
    def gettag(self):
        return self._tag
        
    # Mutators
    def addO(self, O):
        '''Appends an object to <ObjectList>.'''
        self._list.append(O)
        self._len += 1
    def removeO(self, O):
        '''Removes an object from <ObjectList>.'''
        self._list.remove(O)
        self._len -= 1
    def chgtag(self, x):
        self._tag = str(x)