import string
import random

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
	pGene = ''.join(pGene)

	for i in range(len(pGene)):
		thisChar = pGene[i]
		if thisChar == spotValues[i]: return False
		if pGene.count(thisChar) != 2: return False # should be exactly 2!
		#if pCharSet.count(thisChar) == 0: return False # we dont have to do this, because theres no way our genes get contaminated.
		if i % 2 == 0 and (thisChar == pGene[i+1]): return False # catch doubles is they form somehow (mutation).
	return True #kinda a lie - have checkled for invalid chars, dupes "AA" etc.


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

def getTimeAndDist(pLoc1,pLoc2):
	return 300*abs(len(pLoc1)-len(pLoc2))



def theTSPFitness(pGene):
	if not isValidTSPGene(0): return 0

	# least fitness = earth circumference in meters * num cities
	longestDist = 40075160 * len(pGene)
	score = 0
	locPairlist = decode(pGene)
	
	for locPair in locPairList:
		if inCache(locPair):
			pathDetails = getCache(locPair)
		else:
			pathDetails = getTimeAndDist(locPair)
			addToCache(locPair)

			if pathDetails["status"] != 'OK': return 0
			score += pathDetails['distance']

	#fitness
	fitness = longestDist - score
	return fitness

def fileContents(filename):
	txt = open(filename)
	text = txt.read
	txt.close()
	return text

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
	target.write(data)
	target.close
	return True

def addToCache(pLoc1, pLoc2, pData):
	filename = filenameGen(pLoc1,pLoc2)
	writeToFile(filename,pData)

def filenameGen(pLoc1,pLoc2):
	filename = pLoc1 + "_" + pLoc2 + ".txt"
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
	generationNum+=1
	printList(decodeGene(population[0], locCodes, locCodesToValues))

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