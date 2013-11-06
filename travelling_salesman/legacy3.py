#print pathToConnectionsList(['A','C','B','D','E'])
#['EA','CB','AC','BD', 'DE']
#print independantPathPieces()
#print pathToConnectionsList(pathGenerator())
#print geneFormatToPathSegmentsMini(['CD', 'AB', 'BE', 'EC']) #DA
#print independantPathPieces(['EAC', 'CBD', 'ACB', 'BDE', 'DEA'])
#print greedyCrossover(['EC', 'CD', 'AB', 'BE','DF','FA'],['EC', 'XX', 'XX', 'XX','XX','xx'], 3)


#['ABECD', '', '__', '__']

# def joinPathBits(pathBits):
# 	index = 0
# 	for index in range(len(pathBits)):
# 		# figure out nex and prev point
		
# 		while matchFound:
# 			matchFound = False
# 			next = pathBits[index][-1]
# 			prev = pathBits[index][0]

# 			while True
# 			index2 = 1				
# 			if next == pathBits[index2][0] and next != '_':
# 				join one way
# 				matchFound = True
# 			elif prev == pathBits[index2][-1] and prev != '_':
# 				join another
# 				matchFound = True



# def findpaths(segments):
# 	path_starts = {} #  path_start:path
# 	path_ends = {} # path_end:path
# 	starts = {} # start:end of a segment
# 	#path_prefixes = []
# 	for segment in segments:
# 		starts[segment[0]] = segment[1]
# 	for start in starts:
# 		next = segment[start]
# 		if next in starts: # a longer path's been found

def writeToGene(toOrFromPos,whichCodon,whichGene,whatToWrite):
	if toOrFromPos == 'to': pos = 1
	if toOrFromPos == 'from': pos = 0
	#print "which codon: " + str(whichCodon)
	#print "postion: " + str(pos) 
	# check if whichgene[whichcodon is empty]
	
	if whichCodon == 88: return whichGene # this may be the worlds ugliest hack, depending on
	# _ not being a reserved char aka being in the charset but also depending on the num of cities
	# in the prob to be less that 88
	
	spot = whichGene[whichCodon]
	val = whichGene[whichCodon][pos]
	#print "current value: " +  str(val)

	if val == whatToWrite: return whichGene
	if val == "_":
		#spot = ['','']
		#print "spot:"
		#print spot
		spot = list(spot)
		spot[pos] = whatToWrite
		#print "spot:"
		#print spot

		#check if val is empty
		newGene =  whichGene[0:whichCodon] + ["".join(spot)] + whichGene[whichCodon+1:len(whichGene)]
		return newGene
	
	return "ERROR, NON CONSISTANT VALUE ALREADY IN POS."

#print writeToGene('to',2,['__','__','__','__','__','__','xx','xx'],'o')
#writeToGene('to',3,['','','','','','','',''],"x")



def tspGeneTemplater(gene,locCodes):
	# assumes that it gets a valid gene which was constructed by common elements in two parents and an additional random element from on parent.
	gene = codeBlankSpots(gene)
	genecopy = gene
	charset = theCharset()

	for codonLoc in range(len(gene)):
		codon = gene[codonLoc]
		if codon !='__':
			whereFrom = codon[0]
			whereTo = codon[1]
			current = locCodes[codonLoc]

			whereFromIndex = charset.index(whereFrom)  
			whereToIndex = charset.index(whereTo)
			current = locCodes[codonLoc]

			genecopy = writeToGene('from',whereToIndex,genecopy,current)
			genecopy = writeToGene('to',whereFromIndex,genecopy,current)

	#at this point we should have a template!!!!
	# that we can fill in.
	return genecopy

#print tspGeneTemplater(['BD', 'CA', '_B', 'A_'], theCharset())

def templateToGene(gene):
	# GETS A FULLY TEMPLATED GENE
	# MUST NOW FILL UP THE CHARS TO MAKE A VALID GENE! WHAT A DAUNTING TASK!!

	# FIRST WE GET THE CHARSETS WE ARE WORKING WITH
	# ONE FOR TO AND ONE FOR FROM POSITIONS
	#init
	chars = theCharset()[0:len(gene)]
	toChars = chars
	fromChars = chars

	# remove already existing chars
	for codon in gene:
		if codon[0] != "_": fromChars = fromChars.replace(codon[0],'',1)
		if codon[1] != "_":
			toChars = toChars.replace(codon[1],'',1)
		else:
			anEmptyToSpot = gene.index(codon)
			currentLoc = chars[anEmptyToSpot]

	# now we have a list of to and from chars that need to be placed in a valid configuration.
	# choose a blank spot to start from (anEmptyTospot)
	gene = writeToGene('from',anEmptyToSpot,gene,currentLoc)
	cont = True
	while cont:	
		toLoc = random.choice(toChars)
		toChars = toChars.replace(toLoc,'',1)
		gene = writeToGene('from',anEmptyToSpot,gene,currentLoc)

		currentLoc = toLoc

	writeToGene('to',2,['__','__','x_','__','__','__','xx','xx'],'o')
	return connectionList


def geneFormatToPathSegments(gene):
	charset = theCharset()
	segments = []
	for i in range(len(gene)):
		spot = charset[i]
		if gene[i] != '__':
			segment = str(gene[i][0]) + str(spot) + str(gene[i][1])
			segments.append(segment)
	return segments



def indPathPieces(segmentsList):
	for thisSegment in segmentsList:

		for anotherSegment in segmentsList:
			if thisSegment[1:2] == anotherSegment[-2:]:
				newSegment = thisSegment

def independantPathPieces(path_segments = []):
	# TAKES EDGE SEGMENTS FOR EACH GENE OR SOME SUBSET OF GENES AND MAKES A STRING PATH OF MIN LENGTH
	#path_segments = ['LOP','BAC','FYZ','CDF','REX', 'XWL']
	#path_segments = ['EAC','CBD']
	path_segments = ['EA','CB','AC','BD', 'DE']
	# CAREFUL: THERE IS SOME INSANITY LOGIC GOING ON HERE!
	#print "path seg: " + str(path_segments)
	index = 0
	while index < len(path_segments):
		next = path_segments[index][-1]
		
	
		for j in range(len(path_segments)):
			prev = path_segments[j][0]
			print "next: " + next
			print "prev: " + prev
			print "index:" + str(index)
			print path_segments
			if (next == prev) and (next != '_') :
				path_segments[index] = path_segments[index] + path_segments[j][1:]
				path_segments[j] = '_'
				next = path_segments[index][-1]
				#index -=1

			print path_segments
		index +=1
	path_segments = [x for x in path_segments if x != '_']
	#print "path seg: " + str(path_segments)
	return path_segments

	def makeTSPGeneX(numLocations):
	# this time we are going to do things smarter.
	if numLocations < 3 or numLocations > 94:
		print "MAX LOCATIONS IS 94, MIN LOCATIONS IS 3."
		quit()

	# intialize
	locationsCharset =  theCharset()[0:numLocations]
	path =  pathMaker(numLocations)
	#fromLocations = locationsCharset

	locIndex = dict()
	locValue = dict()
	
	# BUILD THE INDEX AND VALUE DICTS
	for i in range(numLocations):
		locIndex[locationsCharset[i]] = i
		locValue[i] = locationsCharset[i]
		connectionList =  ["" for x in range(numLocations)]

	return connectionList


def completeTSPGene(pGene):
	# this time we are going to do things smarter.
	numLocations = len(pGene) 

	# intialize
	locationsCharset =  theCharset()[0:numLocations]
	toLocations = locationsCharset
	fromLocations = locationsCharset

	locIndex = dict()
	locValue = dict()
	
	# BUILD THE INDEX AND VALUE DICTS
	for i in range(numLocations):
		locIndex[locationsCharset[i]] = i
		locValue[i] = locationsCharset[i]
		#connectionList =  ["__" for x in range(numLocations)]

	# remove existing options from charsrets.
	for codon in pGene:
		if codon[0] != "_": fromLocations = fromLocations.replace(codon[0],'',1)
		if codon[1] != "_":
			toLocations = toLocations.replace(codon[1],'',1)
		else:
			# grab details about a codon where the to location is empty. 
			anEmptyToSpot = pGene.index(codon)
			currentLoc = locationsCharset[anEmptyToSpot]

	# we define an empty fromLoc, we have a currentLoc, and we get a toLoc!
	fromLoc = "_"
	#toLoc = random.choice(toLocations)
	#toLocations = toLocations.replace(currentLoc, "")

	
	for i in range(numLocations+1):
		print len(toLocations)
		print len(fromLocations)
		print "wherefrom: "  + fromLoc
		print "currentloc: " + currentLoc
		print "to locs options: " + str(toLocations)
		print "from locs: " + str(fromLocations)
		print pGene
		print 
		#place the from loc in the from position of the current loc
		if fromLoc != "_": 
			pGene[locIndex[currentLoc]] = str(fromLoc) + str(pGene[locIndex[currentLoc]][1])
			fromLocations = fromLocations.replace(fromLoc,'',1)


		if len(toLocations) == 0:
			pGene[locIndex[currentLoc]] = str(fromLoc[0] ) + str(pGene[locIndex[currentLoc]][1])
			return pGene

		toLoc = pGene[locIndex[currentLoc]][1]
		if toLoc == "_":
			# get a to loc only if needed
			#if len(toLocations) == 2 and len(fromLocations) == 1 and (fromLocations == toLoc)

			toLoc = currentLoc
			while (toLoc == currentLoc) or (toLoc == fromLoc) :
				if len(toLocations) == 0:
					toLoc = locValue[anEmptyToSpot]
				else:			
					toLoc = random.choice(toLocations)
			toLocations = toLocations.replace(toLoc, "")

		#place it in the to position of the current loc
		pGene[locIndex[currentLoc]] = str(pGene[locIndex[currentLoc]][0]) + str(toLoc)

		#prepare to move to the new loc!
		fromLoc = currentLoc
		currentLoc = toLoc

	pGene[locIndex[currentLoc]] = str(fromLoc) + str(pGene[locIndex[currentLoc]][0])
	return pGene

#print completeTSPGene(['__','CD','_B','B_','__','__','AC','FI','HA'])