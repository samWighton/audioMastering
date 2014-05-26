#Split string into separate lines
#Split string into separate arguments

#functions will be given arguments in text form



#Current config has the form
#[functionName] , [argument_1] , [argument_2] /r/n
#[functionName] , [argument_1] /r/n

#arguments are always the ID of a track, group, data, 
#def


#    print ('Files processed')
#    print ('Hash =', hashlib.md5('hello there this is a test'.encode()).hexdigest())


import winsound
import sys
import wave
import struct
import math
import hashlib

#main function for isolated testing of functions in this file
#todo remove main function, imports and boilerplate 
def main():
    commandList = splitList('lowPass,4321\r\nhighPass,1234,2345')
    for command in commandList:
        print('args =',splitArgs(command))
        print('  hash =',hashCommand(command))
    return 0

def splitList(givenList):
    return givenList.splitlines()

def splitArgs(givenArgs):
    return givenArgs.split(',')

def hashCommand(givenCommand):
    #will return type 'str'
    #this is used to create an unique identifier to label the output of commands
    #  this prevents identical commands being processed multiple times 
    return hashlib.md5(givenCommand.encode()).hexdigest()

if __name__ == '__main__':
    main()
