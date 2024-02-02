#
# An individual represented by its genotype
# aka a possible solution comprised of different boxes
# for the knapsack problem for A3 Local Search assignment.
# CS 131 - Artificial Intelligence
#
# Written by - Vivian Lau vlau02
# Last modified - 10/30/2023

class Individual:
    
    # Given boxes to make up the solution (individual),
    # assess associated qualities
    # Assumes boxes is an array of tuples in form of (id, weight, importance)
    def __init__(self, boxesIn):
        self.boxes = boxesIn
        self.phenotype = 0
        self.fitness = 0
        self.setPhenotype()
        self.setFitness()
        
    # Returns string version of boxes of the solution individual
    def __str__(self):
        return str(self.boxes)
        
    # Overrides operation to consider that individuals are compared 
    # by the boxes contained in their solution
    def __eq__(self, other):
        return set(self.getGenotype()) == set(other.getGenotype())
        
    # Finds the total weight or cost of the solution
    def setPhenotype(self):
        sumWeights = 0
        for box in self.boxes:
            sumWeights += box[1]
        self.phenotype = sumWeights
    
    # Finds the total importance value of the solution
    def setFitness(self):
        sumImportance = 0
        for box in self.boxes:
            sumImportance += box[2]
        self.fitness = sumImportance
    
    # Returns the total weight or cost of the solution
    def getPhenotype(self):
        return self.phenotype
        
    # Returns the total importance value of the solution
    def getFitness(self):
        return self.fitness
    
    # Returns the length of the solution aka number of boxes used
    def getLength(self):
        return len(self.boxes);
    
    # Given index of the box in the solution
    # returns the information associate with the box
    def getGene(self, index):
        if index >= 0 and index < len(self.boxes):
            return self.boxes[index]
        print("Box was not found!")
        
    # Returns all boxes as an array
    def getGenotype(self):
        return self.boxes