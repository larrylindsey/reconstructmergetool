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
        
    def __str__(self):
        return 'rObject, from series '+self.series.name+', with the name '+str(self.name)
    def returnAtts(self):
        return self.name, self.start, self.end, self.count, self.volume, self.surfacearea, self.flatarea
    def returnChildren(self):
        return self.children
    def popStartendCount(self):
        if self.series != None:
            return self.series.getStartEndCount( self.name )
    def popVolume(self):
        if self.series != None:
            return self.series.getVolume( self.name )
    def popSurfaceArea(self):
        if self.series != None:
            return self.series.getSurfaceArea( self.name )
    def popFlatArea(self):
        if self.series != None:
            return self.series.getFlatArea( self.name )