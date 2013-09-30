import string
import random


def randomString(pLength):
	#RETURN UPPERCASE, lowercase, Numb3rs.
	# Uses this awesome compact method: http://stackoverflow.com/questions/2257441/python-random-string-generation-with-upper-case-letters-and-digits
	return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(pLength))


def solutionFound():
	print("SOLUTION FOUND")
	quit()

def theFitnessOf(pGene):
	#Returns fitness of a particular gene.
	return theLevDist(pGene,theSolution()) 

def theSolution():
	#define solution
	return "HACKER SCHOOL IS AWESOME"

def mutationsOf(pGene):
	#mutates
	return pGene

def theOffspringOf(pGene1,pGene2,pNumChildren):
	#MATES THE TWO GENES USING THE

	offsring = []
	pNumChildren = -1
	#while len(offsring) <= pNumChildren:

	#choose pivot

	
	return pGene

def someRandomGenes(generationSize):
	return [randomString(len(theSolution())) for x in range(generationSize)]

def mainLoop(pGenes):
	## CLEAR VARS

	##INIT
	numchildren = 6

	
	if not pGenes == NULL:
		##CONSTANTS
		generationSize = 1000
		## IF FIRST GEN THEN CREATE FIRST GENERATION
		genes = someRandomGenes(generationSize)
	else:
		generationSize = pGenes.len 

	##SCORE THE FIRST GENERATION
	totalGenFitness = 0 
	for x in range(generationSize):
		if genes[x] == theSolution(): solutionFound()
		geneFitness[x] = theFitnessOf(genes[x])
		totalGenFitness += geneFitness[x]
	avgGenFitness = totalGenFitness/generationSize

	## DELETE / KILL GENES THAT DONT BEAT THE AVERAGE
	for x in range(generationSize):
		### WARNING THIS CODE WONT LOOP PROPERLY I THINK
		if geneFitness[x] <= avgGenFitness: genes.pop(x)

	## MATE THE ONES THAT SURVIVE 
	genes = theOffspringOf[genes]
	genes = mutationsOf[genes]
	mainLoop(genes)

	return NULL

yay = ''.join(['a','b','c','d','e'])
print #yay[0:5]
#len(someRandomGenes(20))




