import string
import random

def theCharset():
	return string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation

def makeTSPGene3(numLocations):
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
	
	for i in range(numLocations):
		locIndex[locationsCharset[i]] = i
		locValue[i] = locationsCharset[i]

	connectionList =  ["" for x in range(numLocations)] 

	# start with first pos in gene
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

	#print connectionList
	#print currentLoc
	#print fromLoc
	#print "left: " + toLocations
	return connectionList

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


def decodeGene(pGene):
	# desired out put - something like - [('Virginia, VA','Columbus, OH'), ('Columbus, OH', 'Dayton,OH')...]



def theTSPFitness(pGene):

	score = 0
	if not isValidTSPGene(0): return 0
	
	for locPair in locPairList:
		pathDetails = getTimeAndDist(locPair)
		if pathDetails["Error"]: return 0

		pathDetails['Distance']









#gene = makeTSPGene3(10)
#print gene

#print isValidTSPGene(gene, theCharset()[0:10])
#print isValidTSPGene(['JJ', 'CG', 'HB', 'EI', 'GD', 'AH', 'BE', 'FC', 'DF', 'IA'], theCharset()[0:10])
#print isValidTSPGene(['EB', 'AC', 'BF', 'IE', 'DA', 'CH', 'JJ', 'FJ', 'GD', 'HG'], theCharset()[0:10])
#print makeValidGene(8,2,0)