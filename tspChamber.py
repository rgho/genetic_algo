import string
import random
import json

def theCharset():
	return string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation

def makeTSPGene(numLocations):
	# this time we are going to do things smarter.
	if numLocations < 3 or numLocations > 94:
		print "MAX LOCATIONS IS 94, MIN LOCATIONS IS 3."
		quit()

	# intialize
	locationsCharset =  theCharset()[0:numLocations]
	toLocations = locationsCharset
	#fromLocations = locationsCharset

	locIndex = dict()
	locValue = dict()
	
	# BUILD THE INDEX AND VALUE DICTS
	for i in range(numLocations):
		locIndex[locationsCharset[i]] = i
		locValue[i] = locationsCharset[i]
		connectionList =  ["" for x in range(numLocations)] 

	# start with first pos in gene, remove it from options.
	fromLoc = ""
	currentLoc = locValue[0]
	toLocations = toLocations.replace(currentLoc, "")

	for i in range(numLocations):
		#place the from loc in the from position of the current loc
		connectionList[locIndex[currentLoc]] = str(fromLoc) + str(connectionList[locIndex[currentLoc]])


		# get a to loc.
		toLoc = currentLoc
		while toLoc == currentLoc:
			if len(toLocations) == 0:
				toLoc = locValue[0]
			else:			
				toLoc = random.choice(toLocations)
				toLocations = toLocations.replace(toLoc, "")

		#place it in the to position of the current loc
		connectionList[locIndex[currentLoc]] = str(connectionList[locIndex[currentLoc]]) + str(toLoc)

		#prepare to move to the new loc!
		fromLoc = currentLoc
		currentLoc = toLoc

	connectionList[locIndex[currentLoc]] = str(fromLoc) + str(connectionList[locIndex[currentLoc]])
	return connectionList

def makeTSPGeneration(populationSize,numLocations):
	population = []
	for i in range(populationSize):
		population.append(makeTSPGene(numLocations))
	return population


def isValidTSPGene(pGene, pCharSet):
	spotValues = "".join([str(pCharSet[i])*2 for i in range(len(pCharSet))])
	pGene = "".join(pGene)

	for i in range(len(pGene)):
		thisChar = pGene[i]
		if thisChar == spotValues[i]: return False
		if pGene.count(thisChar) != 2: return False # should be exactly 2!
		#if pCharSet.count(thisChar) == 0: return False # we dont have to do this, because theres no way our genes get contaminated.
		if i % 2 == 0 and (thisChar == pGene[i+1]): return False # catch doubles if they form somehow (mutation).
	return True #kinda a lie - have checkled for invalid chars, dupes "AA" etc.

def stringToDict(pString):
	thisDict = dict()
	lines = pString.split('\n')
	print lines
	for thisLine in lines:
		thisLine = thisLine.split('=',1)
		print thisLine
		thisDict[thisLine[0]]=thisLine[1]
	return thisDict


def dictToString(dict1):
	string = ""
	for key in dict1:
		string = string + str(key) + "=" + str(dict1[key]) + "\n"
	return string[0:len(string)-1] # delete trailing newline


def decodeGene(pGene, pCharset, plocCodeDict):
	# desired out put - something like - [('Virginia, VA','Columbus, OH'), ('Columbus, OH', 'Dayton,OH')...]
	decoded = []
	for i in range(len(pCharset)):
		currentLoc = plocCodeDict[pCharset[i]]
		prevLoc = plocCodeDict[pGene[i][0]]
		nextLoc = plocCodeDict[pGene[i][1]]

		decoded.append((prevLoc,currentLoc))
		decoded.append((currentLoc,nextLoc))

	# decoded at this point contains all verteces, but the problems
	return list(set(decoded))


def getTimeAndDistGoogleAPI(pLoc1,pLoc2):
	details = dict()
	details['status'] = 'OK'
	details['distance'] = 300*abs(len(pLoc1)-len(pLoc2))
	return details


def getPathDetails(pLoc1,pLoc2):
	if isInCache(pLoc1,pLoc2):
		pathDetails = stringToDict(getCache(pLoc1,pLoc2))
	else:
		pathDetails = getTimeAndDistGoogleAPI(pLoc1,pLoc2)
		addToCache(pLoc1,pLoc2,dictToString(pathDetails))
	return pathDetails


def theTSPFitness(pGene,locCodes,locCodesToValues):
	print pGene
	if not isValidTSPGene(pGene,locCodes): return 0
	# least fitness = earth circumference in meters * num cities
	longestDist = 40075160 * len(pGene)
	score = 0
	locPairList = decodeGene(pGene,locCodes,locCodesToValues)
	for locPair in locPairList:
			pathDetails = getPathDetails(locPair[0],locPair[1])
			if pathDetails["status"] != 'OK': return 0
			score += int(pathDetails['distance'])
	#fitness
	fitness = longestDist - score
	return fitness


def fileContents(filename):
	txt = open(filename)
	text = txt.read()
	txt.close()
	return text


def getCache(pLoc1,pLoc2):
	return fileContents(filenameGen(pLoc1,pLoc2))


def locationsList():
	locs = [line.strip() for line in open('locs.txt')]
	return locs


def isInCache(pLoc1,pLoc2):
	filename = filenameGen(pLoc1,pLoc2)
	return isFile(filename)


def isFile(filename):
	try:
		with open(filename):
			return True
	except IOError:
	   	return False


def writeToFile(filename, data):
	target = open(filename, 'w')
	target.write(str(data))
	target.close
	return True


def addToCache(pLoc1, pLoc2, pData):
	filename = filenameGen(pLoc1,pLoc2)
	writeToFile(filename,pData)


def filenameGen(pLoc1,pLoc2):
	filename = "cache/" + pLoc1 + "_" + pLoc2 + ".txt"
	return filename


def printList(list):
	for i in range(len(list)):
		print list[i]


def mainLoop():
	firstRun = True
	if firstRun:
		# CONSTANTS
		initialPop = 1
		generationNum = 0

		# SETUP
		locationList = locationsList()
		numLocs = len(locationList)
		locCodes = theCharset()[0:numLocs]
		
		# construct a location dict once!
		locCodesToValues = dict()
		for i in range(numLocs):
			locCodesToValues[locCodes[i]] = locationList[i]

		population = makeTSPGeneration(initialPop,numLocs)
		fitnessDetails = theTSPFitness(population[0],locCodes,locCodesToValues)
		print fitnessDetails
	generationNum+=1




mainLoop()

#addToCache("New Delhi, India","Washington DC, USA","AWHOLE BUNCH OF STUFF!")
#print locationsList()
#gene = makeTSPGene(10)
#print decodeGene(gene)

#print gene
#print isValidTSPGene(gene, theCharset()[0:10])
#print isValidTSPGene(['JJ', 'CG', 'HB', 'EI', 'GD', 'AH', 'BE', 'FC', 'DF', 'IA'], theCharset()[0:10])
#print isValidTSPGene(['EB', 'AC', 'BF', 'IE', 'DA', 'CH', 'JJ', 'FJ', 'GD', 'HG'], theCharset()[0:10])
#print makeValidGene(8,2,0)