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



def onePointCrossover(pGene1,pGene2):
	return

def twoPointCrossover(pGene1,pGene2):
	# this should force support of different string lengths
	len1 = len(pGene1)
	len2 = len(pGene2)

	if not len1 == len2:
		if len1 > len2: remnant = pGene1[len2:len1]
		else: remnant = pGene2[len1:len2]

	# how to handle remnant: ignore, trim to average of lens, trim to random size
	geneLength = min(len1,len2)

	# the random function generates random ints within and including the two params
	numCrossovers = 4
	if numCrossovers > geneLength: print "BAD THINGS HAPPEN HERE"

	print range(1,geneLength)
	crossList  = random.sample(range(1,geneLength), numCrossovers)
	print crossList

	for thisCrossover in crossList:
		tempGene1 = pGene1
		pGene1 = pGene1[0:thisCrossover] + pGene2[thisCrossover:geneLength]
		pGene2 = pGene2[0:thisCrossover] + tempGene1[thisCrossover:geneLength]

	print pGene1
	print pGene2

	# for thisCrossover in crossList:
	# 	print thisCrossover
	# 	print pGene1[0:thisCrossover] + pGene2[thisCrossover:geneLength] #+ remnant
	# 	print pGene2[0:thisCrossover] + pGene1[thisCrossover:geneLength] #+ remnant

	return 

def cutAndSplice(pGene1,pGene2):
	return

def uniformCrossover():
	return

def halfUniformCrossover():
	return


twoPointCrossover("XXXXXXXXXXXXXXXXXXXXXXXXX", "OOOOOOOOOOOOOOOOOOOOOOOOO")

