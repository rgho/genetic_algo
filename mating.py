import string
import random

	# def theOffspringOf(pGene1,pGene2,pNumChildren):
	# # NOTE ADD OTHER MATING METHODS
	# #genes must be the same length for this to work correctly.
	# geneLength = len(pGene1) if (len(pGene1) < len(pGene2)) else len(pGene2)
	# offspring = []
	# loopNum = 0
	# while (len(offspring) < pNumChildren) and loopNum < 1000:
	# 	loopNum +=1
	# 	#BY GOING FROM 1 to geneLength-1 we prevent 0 and geneLength from becoming crossover points.
	# 	crossoverPoint = random.randint(1,geneLength-1)

	# 	#generate children
	# 	child1 = pGene1[0:crossoverPoint] + pGene2[crossoverPoint:geneLength]
	# 	child2 =  pGene2[0:crossoverPoint] + pGene1[crossoverPoint:geneLength]

	# 	# add the children to the list
	# 	offspring.append(child1)
	# 	offspring.append(child2)

	# 	return offspring

def twoPointCrossover(pGene1,pGene2,pNumChildren):
	return nPointCrossover(pGene1,pGene2, pNumChildren, 1)

def onePointCrossover(pGene1,pGene2,pNumChildren):
	return nPointCrossover(pGene1,pGene2, pNumChildren, 2)

def nPointCrossover(pGene1,pGene2,pNumChildren,pNumCrossovers):
	# INITIALIZE OFFSPRING LIST
	offspring = []

	# GRAB STR LENGTHS AND DETERMINE GENELENGTH ACCORDINGLY
	len1 = len(pGene1)
	len2 = len(pGene2)
	geneLength = min(len1,len2)
	
	# ASSIGN A VALUE TO THE REMNANT, THE REMAINING CHARS OF THE LONGER GENE
	if len1 == len2: remnant = ""
	elif len1 >	 len2: remnant = pGene1[len2:len1]
	else: remnant = pGene2[len1:len2]

	# DECIDE how to handle remnant: ignore, trim to average of lens, trim to random size
	remnant = remnant

	# DETECT CASE WHERE pNumCrossovers is specified higher than valid
	if pNumCrossovers > geneLength: 
		print "ERROR: NUMBER OF CROSSOVERS MAY NOT EXCEED GENE LENTGH"

	# WE BEGIN GENERATING OFFSRPING TILL WE HAVE ENOUGH!
	loopCount = 0
	while (len(offspring) < pNumChildren) and loopCount < 1000:
		loopCount+=1 #safeguard in case something goes wrong and loops infinitely

		# range(1,geneLength) generates a list of valid crossover points for 
		# the gene (avoiding end charectars 0 and geneLength, which would result in
		# clone on parents. the random.sample returns (pNumCrossover) number of unique
		# and random crossover points from the valid list, in the form of a list.
		randomCrossoverPoints  = random.sample(range(1,geneLength), pNumCrossovers)
		print randomCrossoverPoints

		for thisCrossover in randomCrossoverPoints:
			tempGene1 = pGene1 #because of the destructive nature of the following: 
			# compute offsrping
			pGene1 = pGene1[0:thisCrossover] + pGene2[thisCrossover:geneLength]
			pGene2 = pGene2[0:thisCrossover] + tempGene1[thisCrossover:geneLength]

		# ADD OFFSRPING TO LIST
		offspring.append(pGene1)
		offspring.append(pGene2)

	# FUTURE DEV. IF YOU WANT TO REMOVE DUPES FROM OFFSPRING (THINK THRU IMPLICATIONS)
	# A SET IN PYTHON HAS NO DUPLICATES. SO WE CONVERT OUT LIST TO A SET AND THEN
	# BACK TO A LIST TO PURGE DUPES. NOTE THAT THE ORDER OF THE LIST IS DESTROYED :(
	# offspring = list(set(offspring)). Also note that we would have to add more
	# offsrping to get to the right number of pNumChildren

	# because genes are added 2 at a time sometimes the offspring list will have
	# more genes than we want. so we return the first pNumChildren items. 
	return offspring[0:pNumChildren]

def cutAndSplice(pGene1,pGene2):
	return

def uniformCrossover():
	return

def halfUniformCrossover():
	return

def listPrint(pList):
	for item in pList:
		print item


listPrint(nPointCrossover("XXXXXXXXXXXXXXXXXXXX", "OOOOOOOOOOOOOOOOOOOO", 6, 2))


