class rObject:
    '''rObject contain information for reconstruct objects that requires computation over multiple sections'''
    def __init__(self, name=None, series=None, tag=None):
        self.name = name
        self.series = series
        self.tag = tag
        self.start, self.end, self.count = series.getStartEndCount( self.name )
        self.volume = series.getVolume( self.name )
        self.surfacearea = series.getSurfaceArea( self.name )
        self.flatarea =  series.getFlatArea( self.name )
        self.children = []
        
    def __str__(self):
        return 'rObject, from series '+self.series.name+', with the name '+str(self.name)
    def returnAtts(self):
        return self.name, self.start, self.end, self.count, self.volume, self.surfacearea, self.flatarea