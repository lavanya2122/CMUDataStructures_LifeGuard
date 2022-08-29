import csv
import os

def readFiles():
    # Folder path
    global filename
    print("Hi")
    path = "C:\Life Guard\input"
    os.chdir(path)
    for file in os.listdir(path):
        if file.endswith(".txt"):
            print(file)
            filepath = f"{path}\{file}"
            print(filepath)
            filename = file
            readeachFile(filepath)

def readeachFile(filepath):
    with open(filepath) as file:
        counter = 0
        lifeGuardIntervalsArray = []
        tempArray = [counter - 1]
        for line in file:
            lineStr = line.strip()
            #fileContent = file.readerlines()
            print(lineStr)
            if counter != 0:
                # read each row data and insert start and end dates in array
                tempArray = lineStr.split(" ")
                lifeGuardIntervalsArray.append(tempArray)
            counter = counter + 1
        print(len(lifeGuardIntervalsArray))
        prepareLifeGuardIntervals(lifeGuardIntervalsArray)


def prepareLifeGuardIntervals(lifeGuardIntervalsArray):
    print(lifeGuardIntervalsArray)
    global mysteryCounterDict
    mysteryCounterDict = {}
    for i in range(len(lifeGuardIntervalsArray)):
        checkMaxCoverage(lifeGuardIntervalsArray, i)
    print(mysteryCounterDict)
    keysArray = mysteryCounterDict.keys()
    leastImpactCtr = -1
    highestScore = -1
    for eachKey in keysArray:
        value = mysteryCounterDict.get(eachKey)
        if value > highestScore or highestScore == -1:
            highestScore = value
            leastImpactCtr = eachKey

    print(leastImpactCtr)
    print(highestScore)
    writeToCSV(lifeGuardIntervalsArray, leastImpactCtr)


def checkMaxCoverage(lifeGuardIntervalsArray, mysteryLifeGuardCounter):
    global maxCovered
    maxCovered = 0
    counter = 0
    mysteryLifeGuardSet = set()
    for eachLifeGuardInterval in lifeGuardIntervalsArray:
        if (mysteryLifeGuardCounter != counter):
            # check max coverage here and add them to the set
            for j in range(int(lifeGuardIntervalsArray[counter][0]), int(lifeGuardIntervalsArray[counter][1])):
                mysteryLifeGuardSet.add(j)
        counter = counter + 1
        maxCovered = len(mysteryLifeGuardSet)
    mysteryCounterDict[mysteryLifeGuardCounter] = maxCovered


def writeToCSV(lifeGuardIntervalsArray, ctrToIgnore):
    file_name = filename[0:-4]
    print("file_name=="+file_name)
    file = open(file_name+"_output.txt", "w")
    counter = 0
    print("length==" + str(len(lifeGuardIntervalsArray)))
    for i in range(len(lifeGuardIntervalsArray)):
        if counter != ctrToIgnore:
            print(lifeGuardIntervalsArray[counter])
            file.write(' '.join(lifeGuardIntervalsArray[counter]))
            file.write("\n")
        counter = counter + 1
    file.close()
