import winsound
import sys
import wave
import struct
import math


class c_audio:
    filePath = None
    audioChannels = None
    bitDepth = None
    sampleRate = None
    sampleCount = None
    tracks = None
    def duration(self):
        return self.sampleCount / self.sampleRate

        
def main():
    for i in range(1,len(sys.argv)):
        if is_wav(sys.argv[i]):
            data = openFile(sys.argv[i])
            
            highPassFilter(data, 0.0001)
            outputFile(data)
    print ('Files processed')
    return 0

    
def is_wav(givenString):
    #check if last 4 characters of given string are '.wav'
    if (givenString[-4:] == '.wav'):
        return True
    else:
        return False

def highPassFilter(givenData, halfLife):
    #halfLife in seconds
    rollingAverage = 0
    #geoRatio will be close to 1.0
    geoRatio = pow(0.5,1/(givenData.sampleRate * halfLife))
    tempTrack = []
    for i in range(0,givenData.sampleCount):
        tempTrack.append(int(givenData.tracks[i] - rollingAverage))
        rollingAverage = rollingAverage * geoRatio + givenData.tracks[i] * (1 - geoRatio)
    givenData.tracks = [tempTrack[i] for i in range(givenData.sampleCount)]
    return givenData

def outputFile(givenData):
    splitName = givenData.filePath.split('.')
    splitName[0] = splitName[0]+'_output'
    outputName = '.'.join(splitName)
    
    outputBinary = struct.pack('<' + str(givenData.sampleCount) + 'h' , *givenData.tracks)
    writeFile = wave.open(outputName, 'wb')
    writeFile.setnchannels(givenData.audioChannels)
    writeFile.setsampwidth(int(givenData.bitDepth / 8))
    writeFile.setframerate(givenData.sampleRate)
    writeFile.setnframes(givenData.sampleCount)
    writeFile.setcomptype('NONE', 'not compressed')
    writeFile.writeframesraw(outputBinary)
    writeFile.close()

def openFile(givenFile):
    #open file for reading
    readFile = wave.open(givenFile, 'rb')
    #pull metadata from file
    data = c_audio()
    data.filePath = givenFile
    data.audioChannels = readFile.getnchannels()
    data.bitDepth = readFile.getsampwidth()*8
    data.sampleRate = readFile.getframerate()
    data.sampleCount = readFile.getnframes()
    rawBinary = readFile.readframes(data.sampleCount)
    
    data.tracks = struct.unpack('<' + str(data.sampleCount) + 'h' ,rawBinary)
    readFile.close()
    
    #print
    print('Audio channels =',data.audioChannels)
    print('Bit Depth =',data.bitDepth)
    print('Sample Rate =',data.sampleRate)
    print('Samples =',data.sampleCount)
    print('Length =','{0:.2f}'.format(data.duration()),'seconds')

    return data

    

if __name__ == '__main__':
    main()
