import string
import random
import json
import math
import tspMating as mate
import tspMutations as mutate
import traveltime as travel


def theCharset():
	return string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation

def tspGeneCorrector(gene, numLocations):
	
	return connectionList

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
	for thisLine in lines:
		thisLine = thisLine.split('=',1)
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
	details['distance'] = float(1000*abs(len(pLoc1)-len(pLoc2)))
	return details


def getPathDetails(pLoc1,pLoc2):
	if isInCache(pLoc1,pLoc2):
		#print "used cache"
		pathDetails = stringToDict(getCache(pLoc1,pLoc2))
	else:
		# print "not in cache, called API"
		pathDetails = getTimeAndDistGoogleAPI(pLoc1,pLoc2)
		addToCache(pLoc1,pLoc2,dictToString(pathDetails))
	return pathDetails


def theTSPFitness(pGene,locCodes,locCodesToValues):
	if not isValidTSPGene(pGene,locCodes): return 0
	# least fitness = earth circumference in meters * num cities
	longestDist = 40075160 * len(pGene)
	score = 0
	locPairList = decodeGene(pGene,locCodes,locCodesToValues)
	for locPair in locPairList:
			pathDetails = getPathDetails(locPair[0],locPair[1])
			if pathDetails["status"] != 'OK': return 0
			score += float(pathDetails['distance'])
	#fitness
	fitness = 1000000000000/(score*score)#longestDist - score
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


def mainLoop(currentGeneration, locInfo, generationMeta):
	# CONSTANTS
	mutationProb = 0.3
	matingType = 'onePointCrossover'
	childrenPerParentPair = 100
	initialPop = 1000


	if currentGeneration == None:
		generationMeta = dict()
		generationMeta['number'] = 0 

		# SETUP
		locationList = locationsList()
		numLocs = len(locationList)
		locCodes = theCharset()[0:numLocs]
		
		# construct a location dict once!
		locCodesToValues = dict()
		for i in range(numLocs):
			locCodesToValues[locCodes[i]] = locationList[i]
		population = makeTSPGeneration(initialPop,numLocs)

		locInfo = dict()
		locInfo['locCodes'] = locCodes
		locInfo['locCodesToValues'] = locCodesToValues

	else:
		population = currentGeneration

	# POPULATE GENERATION META DATA
	generationMeta['number'] += 1
	generationMeta['initialPop'] = len(population)
	generationMeta['totalFitness'] = 0
	generationMeta['avgFitness'] = 0
	generationMeta['numFatalGenes'] = 0

	# CALCULATE FITNESS FOR EACH
	generation = dict()
	for gene in population:
		geneHash = "".join(gene)
		generation[geneHash,'fitness'] = theTSPFitness(gene,locInfo['locCodes'],locInfo['locCodesToValues'])
		if generation[geneHash,'fitness'] == 0:
			generationMeta['numFatalGenes'] +=1
		else:
			generation[geneHash,'gene'] = gene
			generationMeta['totalFitness'] += generation[geneHash,'fitness']
			#print str(geneHash) + " " + str(generation[geneHash,'fitness'])

	if (generationMeta['initialPop'] - generationMeta['numFatalGenes']) != 0:
		generationMeta['avgFitness'] = generationMeta['totalFitness'] / (generationMeta['initialPop'] - generationMeta['numFatalGenes'])
	else:
		generationMeta['avgFitness'] = 0

	
	#NOW WE HAVE SOME META INFO, AND A POPULATION WITH FITNESS CALCULATED.
	# NEXT WE REACH SELECTION PHASE

	# NOW WE GRAB A LIST OF THE GENE HASHES AND CALL THEM GENES! SNEAKY.
	genes = list(set([i[0] for i in list(generation.keys())])) # GRAB JUST THE KEYS. INTUITION SAYS KEYS WILL BE TUPLES, WILL HAVE TO FILE GET FIRST ITEM.
	generationMeta['numUnfitToReproduce'] = 0
	for gene in genes:
		# ONE LINER FOR REMOVING BELOW AVG PERFORMERS.
		# NOTE POTENTIAL BUG IF DUPLICATE KEYS EXIST?
		if generation[gene,'fitness'] <= generationMeta['avgFitness']: 
			del generation[gene,'fitness']
			generationMeta['numUnfitToReproduce'] +=1

	
	# A ONE LINE TO MAKE COUPLE OUT OF FIRST AND LAST AND INWARDS OF EACH LIST.
	genes = list(set([i[0] for i in list(generation.keys())])) # make the current genehashes to a list again
	couples = [(generation[genes[i],'gene'],generation[genes[-1-i],'gene']) for i in range(int(math.floor(len(genes)/2)))]
	# INIT KIDS
	kids = []
	for parents in couples:
		# a one liner to add all the kids of parent to the end of the kids list.
		kids.extend(mate.theOffspringOf(parents[0],parents[1],childrenPerParentPair,matingType))

	# for kid in kids:
	# 	# one liner to mutate kids
	# 	kids = mutate.mutate(kids, mutationProb)
	print "==Kids=="
	printList(kids[0:4])

	print "=="
	print "gen num:" + str(generationMeta['number'])
	print "initial pop:" +  str(generationMeta['initialPop'])
	print "totalFitness: "  + str(generationMeta['totalFitness'])
	print "avgFitness: " + str(generationMeta['avgFitness'])
	print "num numFatalGenes: " +  str(generationMeta['numFatalGenes'])
	print "numUnfitToReproduce: " + str(generationMeta['numUnfitToReproduce'])
	print "=="

	keepgoing = raw_input("Continue? ")
	if not keepgoing == 'y':
		quit()
	else:
		mainLoop(kids,locInfo,generationMeta)

mainLoop(None,None,None)