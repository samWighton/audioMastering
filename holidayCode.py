import winsound
import sys
import wave
import struct
import math

def main():
#open file
    #try:
    openFile()
    invertMatrix([[1,2,3],[4,5,6],[7,8,9]])
    #except:
        #print('Error opening file')

#process file
        
#write file
        
#play file
    #playSound(sys.argv[1])

def invertMatrix(givenMatrix):
    #try:
    columnCount = len(givenMatrix[0])
    for row in range(len(givenMatrix)):
        if len(givenMatrix[0]) != columnCount:
            return 0
            #raise

    returnMatrix = []
    for row in range(len(givenMatrix)):
        returnMatrix.append([])
        for column in range(columnCount):
            if column == row:
                returnMatrix[row].append(1)
            else:
                returnMatrix[row].append(0)

    for column in range (columnCount):
        for row in range (len(givenMatrix)):
            pass

    print(givenMatrix)
    print(returnMatrix)
            
    #except:
    #print("Invalid matrix")
    return

def findMirrorPoints(intlist):
    lowestFrequency = 50 #hertz
    sampleRate = 48000 #samples per second
    
    

def findMirrorPointsOld(intList):
    lowestFrequency = 50 #hertz
    sampleWidth = round(48000 / lowestFrequency)
    speedUp = 10
    secondLastResult = 0
    lastResult = 0
    mirrorDict = {}
    for i in range(sampleWidth, len(intList) - sampleWidth,speedUp):
    #for i in range(sampleWidth, sampleWidth+2000,10):
        #print ("sampling at", i / 48000, "seconds")

        maxTotal = 0
        total = 0
        for j in range(sampleWidth):
            total += abs(intList[i + j] - intList[i-j])
            maxTotal += abs(intList[i + j]) + abs(intList[i-j])
        result = total / maxTotal

        if lastResult > secondLastResult and lastResult > result:
            mirrorDict[i-speedUp] = True
        
        #print(result)
        secondLastResult = lastResult
        lastResult = result
    print('mirror count =', len(mirrorDict))
    freq50to100   = 0
    freq100to200  = 0
    freq200to400  = 0
    freq400to800  = 0
    freq800to1600 = 0
    freqAbove1600 = 0
    test = 0
    for i in range(sampleWidth, len(intList) - sampleWidth,speedUp):#make sure this line is the same as loop above
        if i in mirrorDict:
            for j in range(speedUp, sampleWidth, speedUp):
                if i+(j * speedUp) in mirrorDict:
                    test+=1
                    if   48000 / (j * speedUp) < 100:
                        freq50to100+=1
                    elif 48000 / (j * speedUp) < 200:
                        freq100to200+=1
                    elif 48000 / (j * speedUp) < 400:
                        freq200to400+=1
                    elif 48000 / (j * speedUp) < 800:
                        freq400to800+=1
                    elif 48000 / (j * speedUp) < 1600:
                        freq800to1600+=1
                    else:
                        freqAbove1600+=1
                        
    print('Frequency 50 to 100 hz  ', freq50to100)
    print('Frequency 100 to 200 hz ', freq100to200)
    print('Frequency 200 to 400 hz ', freq200to400)
    print('Frequency 400 to 800 hz ', freq400to800)
    print('Frequency 800 to 1600 hz', freq800to1600)
    print('Frequency above 1600 hz ', freqAbove1600)
            
    
def processAudio(intList):
    #draw quick and inaccurate waveform
    scale = 5
    sample = 3000
    total = 0
    for i in range(len(intList)):
        total += abs(intList[i]) / (pow(2,15))
        if i % sample == sample -1:
            position = scale * (10 - math.log(sample / total,2))
            tempString = ""
            for j in range(round(position)):
                if j % scale == 0:
                    tempString += "|"
                else :
                    tempString += "*"
            #print (tempString)
            total = 0
            
    halfLife = 0.05 #in seconds
    geoRatio = pow(0.5,1/(48000 * halfLife))
    print('ratio =', geoRatio)
    rollingAverage = 0
    ago1 = 0
    ago2 = 0
    ago3 = 0
    
    for i in range(len(intList)):        
        rollingAverage = rollingAverage * geoRatio + abs(intList[i]) * (1 - geoRatio)
        if i % sample == sample - 1:
            normalizedAverage = rollingAverage / pow(2,15)
            #print(normalizedAverage)
            position = scale * (20 - math.log(sample / normalizedAverage,2))
            tempString = ""
            for j in range(round(position)):
                if j % scale == 0:
                    tempString += "|"
                else :
                    tempString += "*"
            #print (tempString)
            #print (rollingAverage / pow(2,15))
        lastAccel = ago1 - 2 * ago2 + ago3
        currentAccel = rollingAverage - 2 * ago1 + ago2
        if i % 500 == 0:
            if lastAccel * currentAccel != abs(lastAccel * currentAccel):
                #print("here")
                pass
            
            ago3 = ago2
            ago2 = ago1
            ago1 = rollingAverage
        


def openFile():
    readFile = wave.open(sys.argv[1], 'rb')
    print('Audio channels =',readFile.getnchannels())
    print('Sample width =',readFile.getsampwidth()*8,'bits')
    print('Frame Rate =',readFile.getframerate())
    frameCount = readFile.getnframes()
    print('Frames =',frameCount)
    print('Length =',readFile.getnframes() / readFile.getframerate())
    
    inputBinary = readFile.readframes(frameCount)
    #inputBinary2 = readFile.readframes(48000)
    readFile.close()
    
    splitName = sys.argv[1].split('.')
    splitName[0] = splitName[0]+'_output'
    outputName = '.'.join(splitName)
    print ('file = ' + outputName)
    
    #for i in range(0,48000):
        #inputBinary[i] = inputBinary[i] + inputBinary2[i]
    intlist = struct.unpack('<' + str(frameCount) + 'h' ,inputBinary)
    #data2 = struct.unpack('<48000h',inputBinary2)

    processedIntList = []
    #reverse and add audio to original
    #processedIntList = [round(intlist[i]/2 + intlist[frameCount -1 - i]/2) for i in range(frameCount)]

    findMirrorPoints(intlist)
    
    processedIntList = processAudio(intlist)
    processedIntList = intlist
    
    outputBinary = struct.pack('<' + str(frameCount) + 'h' , *processedIntList)
  
    writeFile = wave.open(outputName, 'wb')
    writeFile.setnchannels(1)
    writeFile.setsampwidth(2)
    writeFile.setframerate(48000)
    writeFile.setnframes(frameCount)
    writeFile.setcomptype('NONE', 'not compressed')
    
    writeFile.writeframesraw(outputBinary)

    writeFile.close()
    
    #playSound(outputName)
    

def playSound(sound):
    winsound.PlaySound(sound, winsound.SND_FILENAME)




if __name__ == '__main__':
    main()
