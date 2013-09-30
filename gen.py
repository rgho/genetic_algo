import string
import random

print random.choice(string.ascii_uppercase)


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

def theOffspringOf(pGene1,pGene2):
	#MATES THE TWO GENES USING THE
	return pGene

def someRandomGenes(generationSize):
	geneLength = theSolution().len 

	genes = []
	for i in range(generationSize):
		genes.append(randomChars(geneLength))


def randomChars(pLength):
	#returns a random string of pLength
	return 1


def mainLoop(pGenes):
	## CLEAR VARS
	
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





