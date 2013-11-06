import string
import random
import json
import math
import tspMutations as mutate
import traveltime as travel
from collections import deque

def theCharset():
	# NO UNDERSCORES
	charset = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
	charset = charset.replace('_','')
	return charset

def edges_to_independant_paths(segments):
    starts_merged = {}
    ends_merged = {}
    for (segstart, segend) in segments:
        # This is the tricky case: joining two known paths
        if segstart in ends_merged and segend in starts_merged:
            start_path = ends_merged[segstart]
            end_path = starts_merged[segend]
            start_path.extend(end_path)
            merged_path = start_path # misomner
            
            # update the start/end to point to the merged path
            starts_merged[merged_path[0]] = merged_path
            ends_merged[merged_path[-1]] = merged_path
            # delete the stale start/end
            del ends_merged[segstart]
            del starts_merged[segend]
        elif segstart in ends_merged:
            current_path = ends_merged[segstart]
            current_path.append(segend)
            ends_merged[segend] = current_path
            del ends_merged[segstart] # no longer a path end
        elif segend in starts_merged:
            current_path = starts_merged[segend]
            current_path.appendleft(segstart)
            starts_merged[segstart] = current_path
            del starts_merged[segend] # no longer a path start
        else:
            starts_merged[segstart] = deque([segstart, segend])
            ends_merged[segend] = starts_merged[segstart] # This *shares* the deques

    return map(lambda x:''.join(x), starts_merged.values())


def pathGenerator(pieces_list):
	# GIVEN peices, GENERATES A RANDOM PATH USING EACH CHAR ONCE
	path = []
	while (len(pieces_list) > 0):
		next = random.choice(pieces_list)
		path.append(next)
		pieces_list.remove(next)

	#FLATTEN?
	#path = ''.join(path)
	return path

def pathToConnectionsList(path, charset):
	# TAKES A PATH and converts it to the edge format of a gene. still needs to be finished.'str' object has no attribute 'append'
	path = path + path[0] +path[1]

	details = dict()
	for i in range(len(path)-2):
		connection = path[i:i+3]
		details[str(connection[1])] = str(connection[0]) + str(connection[2])
	
	#print details
	conList = []
	for i in range(len(charset)):
		conList.append(details[charset[i]])
	return conList

def completePathFromPieces(independantPathPieces, charset):
	#TAKES INDEPENDANT PATHS
	# generate a charset that is the difference of all avail chars and those chars already used in the segments
	alreadyUsedChars = ''.join(independantPathPieces)
	validchars = (set(charset) - set(alreadyUsedChars))
	#now make a list of the independant pieces and the valid chars
	# the | operator unions two sets.
	all_pieces = validchars | set(independantPathPieces)
	all_pieces = list(all_pieces)
	return ''.join(pathGenerator(all_pieces))


def underscore_encode_blank_codons(gene):
	newGene = []
	for codon in gene:
		if codon == '':
			newGene.append("__")
		else:
			newGene.append(codon)
	return newGene

def geneFormatToEdges(gene):
	charset = theCharset()
	segments = []
	for i in range(len(gene)):
		spot = charset[i]
		if gene[i] != '__':
			segment1 = str(gene[i][0]) + str(spot)
			segment2 = str(spot) + str(gene[i][1])
			segments.append(segment1)
			segments.append(segment2)
	# return unique
	return list(set(segments))
	return segments

def tspCrossover(pGene1,pGene2, pNumChildren):	
	offspring = []
	
	# WE BEGIN GENERATING OFFSRPING TILL WE HAVE ENOUGH!
	loopCount = 0
	geneLength = len(pGene1)
	while (len(offspring) < pNumChildren) and loopCount < 50000:
		loopCount+=1 #safeguard in case something goes wrong and loops infinitely

		usedUnmatchedSegment = False
		child = ['' for i in range(geneLength)]
		for charNum in range(geneLength):
			if (pGene1[charNum] == pGene2[charNum]):
				#place this segment into child since both parent have it!
				child[charNum] = pGene1[charNum]
			else:
				#WE WANT EXACTLY ONE SEGMENT FROM ONE PARENT TO MAKE IT IN
				if ((usedUnmatchedSegment == False) and (round(random.uniform(0,1)) == 1)):
					usedUnmatchedSegment = True
					child[charNum] = pGene1[charNum] # A BIT OF A HACK SINCE THE CHILD WILL NEVER
					# GET A UNMATCHED GENE FROM PARENT 2.

		# now we have a valid gene with blank spots!
		# lets fill 'em.
		# code blank spots with '__'
		child = underscore_encode_blank_codons(child)
		#next we convert to segments. # for example RT in the A spot becomes RAT. and so on.
		child = geneFormatToEdges(child)
		#next we remove the redundant parts of the segments
		child = edges_to_independant_paths(child)
		#next we use completePathFromPieces to make it a full string path!
		charset = theCharset()[0:geneLength]
		child = completePathFromPieces(child,charset)
		#finally we convert it back to a gene
		child = pathToConnectionsList(child,charset)

		# if we want these as string we do offspring.append("".join(pGene1)) for both here.
		offspring.append(child)

	return offspring[0:pNumChildren]



def pathMaker(numLocations):
	locationsCharset =  theCharset()[0:numLocations]
	locationsCharset = list(locationsCharset)
	random.shuffle(locationsCharset)
	locationsCharset = "".join(locationsCharset)
	print locationsCharset

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


###################################################
## CACHE

def fileContents(filename):
	txt = open(filename)
	text = txt.read()
	txt.close()
	return text

def getCache(pLoc1,pLoc2):
	return fileContents(filenameGen(pLoc1,pLoc2))

def locationsNames():
	locs = [line.strip() for line in open('locs.txt')]
	return locs

def isInCache(pLoc1,pLoc2):
	filename = filenameGen(pLoc1,pLoc2)
	return isFile(filename)

def isFile(filename):
	#print "looking for: " + filename
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

###################################################################
## FITNESS
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


def theTSPFitness(pGene,locCodes,locCodesToNames):
	if not isValidTSPGene(pGene,locCodes): return 0
	# least fitness = earth circumference in meters * num cities
	longestDist = 40075160 * len(pGene)
	score = 0
	locPairList = decodeGene(pGene,locCodes,locCodesToNames)
	for locPair in locPairList:
			pathDetails = getPathDetails(locPair[0],locPair[1])
			if pathDetails["status"] != 'OK': return 0
			score += float(pathDetails['distance'])
	#fitness
	fitness = 1000000000000/(score*score)#longestDist - score
	return fitness


'''
LOCATION CODE/S : the charecter set that represents each/all location/s.


'''

def mainLoop(currentGeneration, locInfo, generationMeta):
	# CONSTANTS
	mutationProb = 0.3
	matingType = 'tspCrossover'
	childrenPerParentPair = 2
	initialPop = 100

	# CHECK IF THIS IS FIRST GENERATION
	if currentGeneration == None:
		generationMeta = dict()
		generationMeta['number'] = 0 

		# SETUP
		locNames = locationsNames()
		numLocs = len(locNames)
		locCodes = theCharset()[0:numLocs]
		
		# construct a location dict once!
		locCodesToNames = dict()
		for i in range(numLocs):
			locCodesToNames[locCodes[i]] = locNames[i]
		locInfo = dict()
		locInfo['locCodes'] = locCodes
		locInfo['locCodesToNames'] = locCodesToNames

		# create an initial population
		population = makeTSPGeneration(initialPop,numLocs)

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
		# SINCE WE CANT INDEX THE GENES BY THEIR LIST GENES WE FLATTEN THEM AND USE THAT AS AN INDEX.
		geneHash = "".join(gene)
		# CALCULATE THE FITNESS OF EACH GENE
		generation[geneHash,'fitness'] = theTSPFitness(gene,locInfo['locCodes'],locInfo['locCodesToNames'])
		
		if generation[geneHash,'fitness'] == 0:
			generationMeta['numFatalGenes'] +=1
		else:
			# STORE ACTUAL GENE!
			generation[geneHash,'gene'] = gene
			generationMeta['totalFitness'] += generation[geneHash,'fitness']

	# CALCULATE AVG FITNESS OF VALID GENES
	# NOTE: IF WE CAN CONFIRM THAT INVALID GENES ARE NEVER CREATED WE CAN GET RID OF ALL THE CHECKS ON THEM
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
		# HERE IS WHERE WE ARE DOING SELECTION CHOOSING ANYONE BELOW 50% FITNESS.
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
		kids.extend(tspCrossover(parents[0],parents[1],childrenPerParentPair))

	# SHOW SOME OUTPUT.
	print "==Parents=="
	printList(genes[0:10])
	print
	print "==Kids=="
	printList(kids[0:10])

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