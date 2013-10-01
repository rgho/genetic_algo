import string
import random
# import numpy

def theSolution():
	#define solution
	return "HACKER SCHOOL IS AWESOME"

def randomString(pLength):
	#RETURN UPPERCASE, lowercase, Numb3rs.
	# Uses this awesome compact method: http://stackoverflow.com/questions/2257441/python-random-string-generation-with-upper-case-letters-and-digits
	return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(pLength))

def solutionFound():
	print("SOLUTION FOUND")
	quit()

def theFitnessOf(pGene):
	#Returns fitness of a particular gene.
	# the max fitness should be a percentage closeness based on the max length of string.
	sol = theSolution()
	maxFitness = len(sol)
	print maxFitness
	print levDist(pGene, sol)
	print float (maxFitness - levDist(pGene,sol))/(maxFitness)
	return float (maxFitness - levDist(pGene,sol))/(maxFitness)

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




def getxy(grid, x, y):
    return grid[y][x]

def setxy(grid, x, y, val):
    grid[y][x] = val
    return grid

def levDist(pString1, pString2):
# initialize costs
	tLen1 = len(pString1)
	tLen2 = len(pString2)

	tSubCost = 1
	tDelCost = 1
	tAddCost = 1

	
	# the range should be the (len of the string + 1) 
	tDist = [[0 for i in range(tLen1+1)] for j in range(tLen2+1)]

	for x in range(tLen1+1):
		tDist = setxy(tDist,x,0,x)
		for y in range(tLen2+1):
			tDist = setxy(tDist,0,y,y)

			# I DONT UNDERSTAND WHY THESE ARE x-1 and y-1 but it seems to work.
			if pString1[x-1] == pString2[y-1]: 
				tCost = 0
			else:
				tCost = tSubCost

			tMinCost = min((getxy(tDist,x-1,y)+1), (getxy(tDist,x,y-1) + 1), (getxy(tDist,x-1,y-1) + tCost))
			tDist = setxy(tDist,x,y,tMinCost)

	return getxy(tDist,x,y)

	# for x in range(len(pString1)+1):
	# 	tDist[x][0] = x

	# 	for y in range(len(pString2)+1):
	# 		tDist[0][y] = y

	# 		if pString1[x] == pString2[y]: 
	# 				tCost = 0 
	# 		else: 
	# 				tCost = tSubCost
	# 		tDist[x][y] = min((tDist[x-1][y] + 1),(tDist[x][y-1] + 1),(tDist[x-1][y-1] + tCost))

	# return tDist[x][y]


# print levDist("rosettacode", "raisethysword")
# print theFitnessOf("HACKER SCHOOL IS AWESOME")
# print theOffspringOf("TTTTTT", "XXXXXX",10)


generationSize = 10
		## IF FIRST GEN THEN CREATE FIRST GENERATION
genes = someRandomGenes(generationSize)

geneFitness = dict()
generationFitness = 0

for thisGene in genes:
	geneFitness[thisGene] = theFitnessOf(thisGene)
	generationFitness += geneFitness[thisGene]
	print thisGene + "	" + str(geneFitness[thisGene])

avgGenFitness = generationFitness / generationSize
print "AVG GENERATION FITNESS: " + str(avgGenFitness)

print "WHAT HAPPENED THIS GENERATION: "
for thisGene in geneFitness.keys():
	if geneFitness[thisGene] <= avgGenFitness:
		print "DIED WITHOUT REPRODUCING: " + thisGene + "	" + str(geneFitness[thisGene])
		del geneFitness[thisGene]

# ASSIGN SURVIVING GENES
genes = geneFitness.keys()
offspring = []
print 

if len(genes) > 2:
	offspring.append(theOffspringOf(genes[-1],genes[1]))
	#get rid of first and last itmes
	genes.pop(0)
	genes.pop(-1)



for thisGene in genes:
	
	print "REPRODUCED: " + thisGene + "	" + str(geneFitness[thisGene])




	# ##SCORE THE FIRST GENERATION
	# totalGenFitness = 0 
	# for x in range(generationSize):
	# 	if genes[x] == theSolution(): solutionFound()
	# 	geneFitness[x] = theFitnessOf(genes[x])
	# 	totalGenFitness += geneFitness[x]
	# avgGenFitness = totalGenFitness/generationSize

