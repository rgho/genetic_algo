import string
import random
import json
import tspMating as mate
import tspMutations as mutatate
import traveltime as travel


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
	details['distance'] = 300*abs(len(pLoc1)-len(pLoc2))
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


def mainLoop(currentGeneration):
	if currentGeneration == None:
		# CONSTANTS
		childrenPerParentPair = 6
		initialPop = 100
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


	generationMeta['number'] += 1
	generation['initialPop'] = len(population)
	generationMeta['totalFitness'] = 0
	generationMeta['avgFitness'] = 0

	# CALCULATE FITNESS FOR EACH
	generation = dict()
	generationMeta['totalFitness'] += generation[geneHash,'fitness']
	for gene in population:
		geneHash = "".join(gene)
		generation[geneHash,'fitness'] = theTSPFitness(gene,locCodes,locCodesToValues)
		generation[geneHash,'gene'] = gene
		generationMeta['totalFitness'] += generation[geneHash,'fitness']
		print str(geneHash) + " " + str(generation[geneHash,'fitness'])

	generationMeta['avgFitness'] = generationMeta['totalFitness'] / generationMeta['initialPop']
	
	##INIT
	numchildren = 6



	## INTIALIZE A DICTIONARY TO STORE GENE FITNESS AND A VAR TO STORE
	## TOTAL GENERATION FITNESS
	geneFitness = dict()
	generationFitness = 0

	## CALCULATE FITNESS FOR EACH GENE, STORE IN DICT AND PRINT
	for thisGene in genes:
		geneFitness[thisGene] = theFitnessOf(thisGene)
		generationFitness += geneFitness[thisGene]
		print "		" + thisGene + "						" + str(geneFitness[thisGene])

	## DETERMINE GENERATIONAL AVERAGE AND PRINT
	avgGenFitness = float(generationFitness) / generationSize
	print "AVG GENERATION FITNESS: " + str(avgGenFitness)

	## KILL GENES THAT DID NOT PERFORM ABOVE AVERAGE
	## PRODUCE REPORT FOR DEATHS AND REPRODUCTION
	test1 = len(geneFitness.keys())
	print "WHAT HAPPENED... GENERATION # " + str(pGenerationNum) + " :" 
	for thisGene in geneFitness.keys():
		if geneFitness[thisGene] >= avgGenFitness:
			print "DIED W/O REPRODUCING:	 " + thisGene + "						" + str(geneFitness[thisGene])
			del geneFitness[thisGene]

	# ASSIGN SURVIVING GENES TO THE MAIN GENES LIST
	test2 = len(geneFitness.keys())
	genes = geneFitness.keys()
	
	## INIT EMPTY OFFSPRING LIST
	offspring = []	
	print 

	## PRODUCE REPORT ON 
	# for thisGene in genes:
	# 	print "REPRODUCED: " + thisGene + "	" + str(geneFitness[thisGene])

	## CHOOSE MATES (FIRST AND LAST ITEMS IN LIST) PRODUCE OFFSPRING AND REPORT
	

	while len(genes) >= 2:
		# print "==FAMILY=="
		# print "PARENT1: " + genes[0] + "	" + str(geneFitness[genes[0]])
		# print "PARENT2: " + genes[-1] + "	" + str(geneFitness[genes[-1]])
		newOffspring = theOffspringOf(genes[-1],genes[0],numchildren)
		offspring.append(newOffspring)
		# print "OFFSPRING: " + str(newOffspring)
		# print "====="
		#get rid of first and last itmes now that they have reporduced, they die. their children live on.
		genes.pop(0)
		genes.pop(-1)


	# FORMAT THE OFFSPRING LIST
	# flattens the weirdly nested list of offspring http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python

	offspring = [item for sublist in offspring for item in sublist]
	print
	print "NUM DIED: " + str(test1-test2)
	print "GENERATION # " + str(pGenerationNum) + " :" 
	print "NUM KIDS: " + str(len(offspring))
	print "AVG PARENTS' GENERATION FITNESS: " + str(avgGenFitness)

	## SINCE THE OFFSPRING IS THE NEW GENERATION, THEY BECOME THE genes LIST:
	pGenerationNum += 1 
	#genes = offspring

	keepgoing = raw_input("Continue? ")
	if not keepgoing == 'y':
		quit()
	else:
		mainLoop(offspring,pGenerationNum)





mainLoop()