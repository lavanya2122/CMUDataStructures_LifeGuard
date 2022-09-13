from operator import attrgetter
import csv
import os
import time

lifeGuardIntervalsArray = []

class lifeGuardShift:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        if (end > start):
            self.duration = end - start
        else:
            self.duration = 0

def readFiles():
    # Folder path
    global filename
    global currentTime
    currentTime = time.time() * 1000
    path = "C:\Life Guard\input"
    os.chdir(path)
    for file in os.listdir(path):
        if file.endswith(".txt"):
            print(file)
            filepath = f"{path}\{file}"
            print(filepath)
            filename = file
            readeachFile(filepath)
sortedIntervalsArray = []
def readeachFile(filepath):
    with open(filepath) as file:
        counter = 0
        tempArray = [counter - 1]
        for line in file:
            lineStr = line.strip()
            #fileContent = file.readerlines()
            #print(lineStr)

            if counter != 0:
                # read each row data and insert start and end times in array
                tempArray = lineStr.split(" ")
                if(len(tempArray)==2):
                    startTime = tempArray[0]
                    endTime = tempArray[1]
                    lifeGuardIntervalsArray.append(lifeGuardShift(int(startTime), int(endTime)))
            counter = counter + 1

        #sort list of lifeguards array by start time
        sortedIntervalsArray = lifeGuardIntervalsArray.sort(key=lambda x:x.start)

        #for eachLifeGuard in lifeGuardIntervalsArray:
            #print(str(eachLifeGuard.start)+" "+str(eachLifeGuard.end))

        prepareLifeGuardIntervals(lifeGuardIntervalsArray)
        #calculateOverlapIntervals()

ignoredIntervals = 0
def calculateOverlapIntervals():
    print("in overlap intervals..")
    startTime = -1
    endTime = -1
    counter = 0
    totalCoverage = 0
    ignoredIntervals = 0
    for eachLifeGuard in lifeGuardIntervalsArray:
        if counter == 0:
            startTime = eachLifeGuard.start
            endTime = eachLifeGuard.end
        else:
            #compare start times with subsequent time intervals
            currentShiftStart = eachLifeGuard.start
            currentShiftEnd = eachLifeGuard.end

            isStartTimeIntersecting = False
            isStartTimeSubset = False

            # current time intersects with start time
            isStartTimeIntersecting = isStartTimeIntersectsCurrentTime(startTime, endTime, currentShiftStart,
                                                                       currentShiftEnd)
            if(isStartTimeIntersecting):
                endTime = currentShiftEnd
                print("duration=="+endTime - startTime)
                continue
            #start time is subset of current time
            isStartTimeSubset = isStartTimeSubsetofCurrentTime(startTime, endTime,currentShiftStart,currentShiftEnd)
            if(isStartTimeSubset):
                ignoredIntervals = ignoredIntervals + 1
                continue
            totalCoverage = totalCoverage + (endTime - startTime)
            startTime = currentShiftStart
            endTime = currentShiftEnd

        totalCoverage = totalCoverage + (endTime - startTime)
        #print("ignoredIntervals=="+str(ignoredIntervals))
        #print("totalCoverage=="+str(totalCoverage))

def isStartTimeSubsetofCurrentTime(startTime, endTime,currentShiftStart,currentShiftEnd):
    if (startTime >= currentShiftStart and endTime <= currentShiftEnd):
        isStartTimeSubset = True
        endTime = currentShiftEnd
    else:
        isStartTimeSubset = False
    return isStartTimeSubset

def isStartTimeIntersectsCurrentTime(startTime, endTime,currentShiftStart,currentShiftEnd):
    print("start time intersects")
    if (currentShiftStart <= endTime):
        isStartTimeIntersecting = True
    else:
        isStartTimeIntersecting = False


def prepareLifeGuardIntervals(lifeGuardIntervalsArray):
    #print(lifeGuardIntervalsArray)
    global mysteryCounterDict
    mysteryCounterDict = {}
    for i in range(len(lifeGuardIntervalsArray)):
        checkMaxCoverage(lifeGuardIntervalsArray, i)

    if len(mysteryCounterDict) > 0:
        print(mysteryCounterDict)
        valuesArray = mysteryCounterDict.values()
        if len(valuesArray) > 0:
            maxValue = max(valuesArray)
            print("maxValue=="+str(maxValue))
            writeToCSV(maxValue)


def checkMaxCoverage(lifeGuardIntervalsArray, mysteryLifeGuardCounter):
    global maxCovered
    maxCovered = 0
    counter = 0
    mysteryLifeGuardSet = set()
    for eachLifeGuardInterval in lifeGuardIntervalsArray:
        if (mysteryLifeGuardCounter != counter):
            # check max coverage here and add them to the set
            start = eachLifeGuardInterval.start
            end = eachLifeGuardInterval.end
            for j in range(int(start), int(end)):
                mysteryLifeGuardSet.add(j)
        counter = counter + 1
        maxCovered = len(mysteryLifeGuardSet)
    mysteryCounterDict[mysteryLifeGuardCounter] = maxCovered


def writeToCSV(maxValue):
    file_name = filename[0:-4]
    print("file_name=="+file_name)
    file = open(file_name+"_output.txt", "w")
    file.write(str(maxValue))
    file.close()
    endTime = time.time() * 1000
    totalTime = currentTime - endTime
    print("totalTime in milli seconds=="+str(totalTime))