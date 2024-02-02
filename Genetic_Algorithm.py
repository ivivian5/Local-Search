#
# Genetic (Local) search algorithm for A3 Local Search assignment.
# CS 131 - Artificial Intelligence
#
# Written by - Vivian Lau vlau02
# Last modified - 10/30/2023

import random # to randomly choose parents
import math # to round floats to integers
from Individual import Individual 

class GeneticAlgorithm:
    
    # Given different boxes and the limit to the solution of boxes
    # Boxes are in form of a tuple of integers in form of: (weight, importance)
    # Limit to solution of box is integer of max weight for valid solution
    def __init__(self, boxesIn, solutionLimitIn):
        self.boxes = []
        for i in range(len(boxesIn)): # index number is id of box (duplicates)
            self.boxes.append((i,) + boxesIn[i])
        self.solutionLimit = solutionLimitIn
        
    # Returns sorted population comprised of the best of given percentage 
    # of individuals which is determined by the fitness of the individuals
    # sorted population starts from best to worse
    def culling(self, population, percentage):
        # sort population by its fitness
        population.sort(key = lambda individual: individual.getFitness(), \
                        reverse = True)
        
        # choose how many of the best individuals to keep
        numKeep = math.ceil(percentage*len(population))
        
        # make new population
        newPopulation = []
        
        # must keep at least two individuals of old population (as parents)
        # as long as old population has at least two individuals
        if (len(population) >= 2 and numKeep < 2):
            numKeep = 2
        elif numKeep < 2:
            numKeep = len(population)
        
        # add best individuals of old population to new population
        for i in range(numKeep):
            newPopulation.append(population[i])
        
        return newPopulation
            
        
    # Given a genotype, modifies genotype by mutation of adding a gene
    def mutateAdd(self, genotype):
        if (len(genotype) < len(self.boxes)): # exists more genes to swap with
            # find all box genes that are currently missing from solution
            geneOptions = list(set(self.boxes).difference(set(genotype)))
            
            # choose one of the available genes
            chosenGeneIndex = random.randint(0, len(geneOptions)-1)
            
            # add the gene
            genotype.append(geneOptions[chosenGeneIndex])
        
    # Given a genotype, modifies genotype by mutation of swapping one gene
    def mutateSwap(self, genotype):
        if (len(genotype) < len(self.boxes)): # exists more genes to swap with
            # find all box genes that are currently missing from solution
            geneOptions = list(set(self.boxes).difference(set(genotype)))
            
            # choose one of the available genes
            chosenGeneIndex = random.randint(0, len(geneOptions)-1)
            
            # choose a existing gene in the genotype to swap with
            swapGeneIndex = random.randint(0, len(genotype)-1)
            
            # swap the original gene with new gene
            genotype[swapGeneIndex] = geneOptions[chosenGeneIndex]
        
    # Returns a child given two possible parent gene solutions
    def reproduce(self, parent1, parent2):
        # choose where one-point crossover will occur for both parent genes
        p1crossIndex = random.randint(0, parent1.getLength()-1)
        p2crossIndex = random.randint(0, parent2.getLength()-1)
        
        # make child
        childGene = []
        
        if (random.randint(1,2) == 1): # pick which parent as first half
            for i in range(p1crossIndex):
                childGene.append(parent1.getGene(i))
            for i in range(p2crossIndex, parent2.getLength()):
                childGene.append(parent2.getGene(i))
        else:
            for i in range(p2crossIndex):
                childGene.append(parent2.getGene(i))
            for i in range(p1crossIndex, parent1.getLength()):
                childGene.append(parent1.getGene(i))
        childGene = list(set(childGene)) # get rid of duplicate genes
        
        # probability of mutate
        mutateProb = random.randint(1,10)
        
        # mutate child
        if mutateProb == 1: # add new gene mutation
            self.mutateAdd(childGene)
        elif mutateProb == 2: # swap existing gene mutation
            self.mutateSwap(childGene)
        # otherwise don't mutate
        
        return Individual(childGene)
        
    # Returns true if the child if fit to be a solution, false otherwise
    def isFit(self, child):
        return child.getPhenotype() <= self.solutionLimit
    
    # Prints ID of each box in given solution individual
    def printBoxID(self, individual):
        for box in individual:
            print(box[0], end=",")
        print()
        
    # Prints each solution individual in a given population
    def printPopulation(self, population):
        for individual in population:
            print("\t", individual.__str__())
        print()
        
    # Returns a solution to the problem given original population
    # that is optimized by the genetic algorithm (not guaranteed optimal)
    # Takes in population to reproduce with and number of generations
    def findSolution(self, population, numGenerations, origNumGen):
        # print current generation
        print("   Generation",(origNumGen-numGenerations+1),":")
        self.printPopulation(population)
        print ("----------------------------------------------------------------------")
        
        nextGen = [] # next generation of individuals
        
        # cull half of the population
        nextGen = self.culling(population, 0.5)
        
        # FOR TESTING
        #print("After Culling:")
        #self.printPopulation(nextGen)
        
        # if population completely dead, no solution found
        if (nextGen is None or len(nextGen) == 0):
            return None
        
        # if simulation is done, return best solution found
        if (numGenerations == 1):
            return nextGen[0] # assumes that individuals are sorted by fitness
        
        # repeat in filling rest of generation with offspring
        for i in range(math.ceil(len(population)/2), len(population)):
            # select two random parents
            p1Index = p2Index = 0 # index of next generation individuals
            while p1Index == p2Index: # repeat until parents are different parents
                p1Index = random.randint(0, len(nextGen)-1)
                p2Index = random.randint(0, len(nextGen)-1)
                
            # make a child
            child = self.reproduce(nextGen[p1Index], nextGen[p2Index])
            # while child not fit or already in population
            while (not self.isFit(child)) or \
                     any(child == individual for individual in nextGen):
                # keep making children
                child = self.reproduce(nextGen[p1Index], nextGen[p2Index])
            
            # add newfound child to next generation
            nextGen.append(child)
            
            # FOR TESTING
            #print ("Adding new solution:", child)
        
        # repeat process with next generation
        return self.findSolution(nextGen, numGenerations-1, origNumGen)
    
    # Runs findSolution from given boxes as the initial population
    # for the genetic algorithm
    # Takes number of generations to run the algorithm for
    def run(self, numGenerations):
        firstGen = []
        
        for box in self.boxes:
            tempIndiv = [] # temporary individual 
            
            # check if box is plausible solution
            if box[1] <= self.solutionLimit:
                # each initial solution only has one box
                tempIndiv.append(box)
                # add possible initial solution
                firstGen.append(Individual(tempIndiv))
        
        # run the solution on the first generation for given number of generations
        return self.findSolution(firstGen, numGenerations, numGenerations)