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

def theOffspringOf(pGene1,pGene2):
	#MATES THE TWO GENES USING THE
	return pGene

def someRandomGenes(generationSize):
	return randomString(len(theSolution())for x in range(generationSize)







print randomString(20)
print someRandomGenes(20)




