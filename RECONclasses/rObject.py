import operator
class rObject:
    '''rObject contain information for reconstruct objects that requires computation over multiple sections'''
    def __init__(self, name=None, series=None, tag=None):
        self.name = name
        self.series = series
        self.tag = tag
        self.start, self.end, self.count = self.popStartendCount()
        self.volume = self.popVolume()
        self.surfacearea = self.popSurfaceArea()
        self.flatarea =  self.popFlatArea()
        self.children = []     
    def __getitem__(self, index):
        if type(index) == str:
            return self.children[operator.indexOf([child.name for child in self.children],index)]
        elif type(index) == int:
            return self.children[index]
        else:
            return None
    def __str__(self):
        return 'rObject, from series '+self.series.name+', with the name '+str(self.name)
    
    def returnAtts(self):
        return self.name, self.start, self.end, self.count, self.volume, self.surfacearea, self.flatarea
    
    def returnChildren(self):
        return self.children
    
    def popStartendCount(self):
        try:
            return self.series.getStartEndCount( self.name )
        except:
            return None
    
    def popVolume(self):
        try:
            return self.series.getVolume( self.name )
        except:
            return None
        
    def popSurfaceArea(self):
        try:
            return self.series.getSurfaceArea( self.name )
        except:
            return None
        
    def popFlatArea(self):
        try:
            return self.series.getFlatArea( self.name )
        except:
            return None