class xmlOut():
    def __init__(self, inObject):
        if inObject._tag == 'Series':
            self._header = '<?xml version="1.0"?>\n<!DOCTYPE Series SYSTEM "series.dtd">\n'
        elif inObject._tag == 'Section':
            self._header = '<?xml version="1.0"?>\n<!DOCTYPE Section SYSTEM "section.dtd">\n'
        
    def __str__(self):
        return self._header