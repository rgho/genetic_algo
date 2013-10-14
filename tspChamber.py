import string
import random

def theCharset():
	return string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation

def makeValidGene(pNumSpots,pNumCharsPerSpot, pUniqueInSpot):
	lenCharSpace = pNumSpots * pNumCharsPerSpot
	
	gene = []
	for spotIndex in range(pNumSpots):
		charset = theCharset()[0:lenCharSpace]
		spotValue = charset[spotIndex]

		spot = ""
		for charIndexInSpot in range(pNumCharsPerSpot):
			candidateFound = False
			while candidateFound != True:
				candidate = random.choice(charset)
				#candidate = 
				#print candidate + " " + spotValue
				if candidate != spotValue:
					# CRITICAL THE FOLLOWING LINE ONLY WORKS IF THERE IS ONE INSTANCE OF EACH CHAR
					# IN THE CHAR SET. WILL FAIL IF CHARSET LOOKS LIKE "XXXXXXYYYYYY" FOR EXAMPLE
					# THIS IS THE NAIVE WAY OF GUARENTEEING UNIQUE NESS ACCROSS GENE AND SPOT.
					charset = charset.replace(candidate, "")
					spot = spot + str(candidate)
					#print spot
					break

		gene.append(spot)
	return gene

def makeTSPGene(numLocations):
	if numLocations < 3 or numLocations > 94:
		print "MAX LOCATIONS IS 94, MIN LOCATIONS IS 3."
		quit()

	# intialize from and to char sets.
	locationsCharset =  theCharset()[0:numLocations]
	fromCharset = locationsCharset
	toCharset = locationsCharset
	
	# connections will store the 
	connections = []
	for i in range(numLocations):
		originLoc = locationsCharset[i]

		# get from candidate that doesnt match origin loc
		candidateFrom = originLoc # initialize in a way the forces it to enter the while loop
		while candidateFrom == originLoc:
			candidateFrom = random.choice(fromCharset)
			print "==FROM=="
			print originLoc + ":" + candidateFrom + ":choices{" + fromCharset 

		# get to candidate that doesnt match from candidate or origin loc
		candidateTo = originLoc # initialize in a way the forces it to enter the while loop
		while (candidateTo == originLoc) or (candidateTo == candidateFrom):
			candidateTo = random.choice(toCharset)
			print "==TO=="
			print originLoc + ":" + candidateTo + ":choices{" + toCharset 

		# remove successfull from candidate from the fro charsets
		# so they it longer appear as a from location. same for to candidate.
		fromCharset = fromCharset.replace(candidateFrom, "")
		toCharset = toCharset.replace(candidateTo,"")

		#write to gene
		connections.append(str(candidateFrom) + str(candidateTo))

	print connections


def makeTSPGene2(numLocations):
	# this time we are going to do things smarter.
	if numLocations < 3 or numLocations > 94:
		print "MAX LOCATIONS IS 94, MIN LOCATIONS IS 3."
		quit()

	# intialize
	locationsCharset =  theCharset()[0:numLocations]
	connectionDict = dict()
	lastLoc = None
	currentLoc = None
	nextLoc = None

	# init last and current
	starterLoc = random.choice(locationsCharset)
	lastLoc = starterLoc
	locationsCharset = locationsCharset.replace(lastLoc, "")
	currentLoc = random.choice(locationsCharset)
	locationsCharset = locationsCharset.replace(currentLoc, "")

	for i in range(numLocations-2):
		# compute next link
		nextLoc = random.choice(locationsCharset)
		locationsCharset = locationsCharset.replace(nextLoc, "")
		
		# build a connection and add to gene
		connectionDict[currentLoc] = str(lastLoc) + str(nextLoc)  # needs to place based on currentLoc

		# now we imagine we have the next connection forward so we update our
		# last and current loc accoridingly, so that we dont trigger intializion
		# on the next iteration.
		lastLoc = currentLoc
		currentLoc = nextLoc

	#finally we connect the last position to the first on outside the loop.
	connectionDict[currentLoc] = str(lastLoc) + str(starterLoc)
	print connectionDict



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


#gene = makeTSPGene3(10)
#print gene

#print isValidTSPGene(gene, theCharset()[0:10])
#print isValidTSPGene(['JJ', 'CG', 'HB', 'EI', 'GD', 'AH', 'BE', 'FC', 'DF', 'IA'], theCharset()[0:10])
#print isValidTSPGene(['EB', 'AC', 'BF', 'IE', 'DA', 'CH', 'JJ', 'FJ', 'GD', 'HG'], theCharset()[0:10])
#print makeValidGene(8,2,0)