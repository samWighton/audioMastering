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
            highPassFilter(data, 0.001)
            findStartOfSine(data)
            outputFile(data)
    print ('Files processed')
    return 0

def findStartOfSine(givenData,requiredAmplitude = 0.001):
    #Find points in the file where
    #the waveform crosses from negative to positive
    #signifying (probably) the start of a cycle
    #of the sine wave that is the 'base frequency'
    #of a sample
    points = []
    maxAmplitude = 0

    #tempTrack = []
    #tempTrack.append(int(givenData.tracks[0]))
    
    for i in range(1,givenData.sampleCount):
        #tempTrack.append(int(givenData.tracks[i]))
        if abs(givenData.tracks[i]) > maxAmplitude:
            maxAmplitude = abs(givenData.tracks[i])
        if givenData.tracks[i - 1] <= 0 and givenData.tracks[i] > 0:
            if (maxAmplitude > requiredAmplitude * pow(2,givenData.bitDepth - 1)):
                #tempTrack[-1] = int(pow(2,givenData.bitDepth - 2))
                maxAmplitude = 0
                points.append(i)
    print("Points Found = ", len(points))
    calculateFrequency(givenData,points,50)
    #givenData.tracks = [tempTrack[i] for i in range(givenData.sampleCount)]
    return None

def calculateFrequency(givenData,points,lowestFrequency = 50):
    #look at distance between start of sinewaves to approximate 'base frequency'
    gaps = []
    for i in range(len(points)):
        if i % 1000 == 999:
            drawCumulative(givenData, gaps, points[i])
            gaps = []
        for j in range(i+1,i+3):#3 is arbitrary. todo, make this line better
            if j >= len(points):
                break
            if points[j] - points[i] > givenData.sampleRate / lowestFrequency:
                break
            gaps.append(points[j] - points[i])
    #print('number of gaps = ', len(gaps))
            
def drawCumulative(givenData, gaps, startAt):
    print('number of gaps = ', len(gaps))
    if startAt >= givenData.sampleCount - 1000:
        return None
    #create tempTrack, ready to edit
    tempTrack = []
    for i in range(givenData.sampleCount):
        tempTrack.append(int(givenData.tracks[i]))
    counter = 0
    for i in range(startAt, startAt+1000):
        counter = 0
        for j in range(len(gaps)):
            if gaps[j] < i - startAt:
                counter+=1
        tempTrack[i] = int(pow(2,givenData.bitDepth - 2) * counter / len(gaps))#
    givenData.tracks = [tempTrack[i] for i in range(givenData.sampleCount)]
            
    
def is_wav(givenString):
    #check if last 4 characters of given string are '.wav'
    if (givenString[-4:] == '.wav'):
        return True
    else:
        return False

def highPassFilter(givenData, halfLife = 0.001):
    #halfLife in seconds
    #could be improved by starting at average of a quick sample of audio
    #  rather than 0
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
