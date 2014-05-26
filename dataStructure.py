class dataStructure:
    """Defines the 'getType()' function"""
    #underlying data structure for all types of data
    #has the type and a metaData dictionary
    structureType = 'Not allocated'
    metaData = {}
    def getType(self):
        return self.structureType

class track(dataStructure):
    """Stores a value that changes over time"""
    def getValueAt():
        pass
    def __init__(self):
        self.structureType = 'track'

class dot_track(track):
    """List of 'value at time' data, then join the dots"""
    #data is stored as a list of 'value at time' points
    #value assumed to change linearly between points
    def getValueAt():
        pass
    
class equation_track(track):
    """Other tracks and maths operators are used to form this track"""
    def getValueAt():
        pass

class group(dataStructure):
    """A group can contain tracks and other groups"""
    #tracks that should be processed together should be in a group
    def __init__(self):
        self.structureType = 'group'

class information(dataStructure):
    """Advanced info required by complex commands"""
    #could contain data describing vocal characteristics of several people
    #to identify which person is talking 
    def __init__(self):
        self.structureType = 'information'
        
