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
	#genes must be the same length for this to work correctly.
	geneLength = len(pGene1)
	offspring = []
	loopNum = 0
	while (len(offspring) < pNumChildren) and loopNum < 1000:
		loopNum +=1
		#BY GOING FROM 1 to geneLength-1 we prevent 0 and geneLength from becoming crossover points.
		crossoverPoint = random.randint(1,geneLength-1)

		#generate children
		child1 = pGene1[0:crossoverPoint] + pGene2[crossoverPoint:geneLength]
		child2 =  pGene2[0:crossoverPoint] + pGene1[crossoverPoint:geneLength]

		# add the children to the list
		offspring.append(child1)
		offspring.append(child2)

	return offspring

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

print theOffspringOf("TTTTTT", "XXXXXX",10)









