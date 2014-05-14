import winsound
import sys
import wave
import struct
import math

class c_track:
    pass

class c_audio:
    audioChannels = None
    bitDepth = None
    sampleRate = None
    sampleCount = None
    def duration(self):
        return self.sampleCount / self.sampleRate
    tracks = c_track()

def main():
    for i in range(1,len(sys.argv)):
        if is_wav(sys.argv[i]):
            openFile(sys.argv[i])
    print ('Files processed')
    return 0
    
def is_wav(givenString):
    #check if last 4 characters of given string are '.wav'
    if (givenString[-4:] == '.wav'):
        return True
    else:
        return False


def openFile(givenFile):
    #open file for reading
    readFile = wave.open(givenFile, 'rb')
    #pull metadata from file
    data = c_audio()
    data.audioChannels = readFile.getnchannels()
    data.bitDepth = readFile.getsampwidth()*8
    data.sampleRate = readFile.getframerate()
    data.sampleCount = readFile.getnframes()
    rawBinary = readFile.readframes(data.sampleCount)
    
    #data.tracks(struct.unpack('<' + str(data.sampleCount) + 'h' ,rawBinary))
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
