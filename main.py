#
# main function for A3 Local Search assignment.
# Uses genetic algorithm to solve knapsack problem.
# CS 131 - Artificial Intelligence
#
# Written by - Vivian Lau vlau02
# Last modified - 10/30/2023


from Genetic_Algorithm import GeneticAlgorithm

print ("----------------------------------------------------------------------")
print("Welcome to Vivian's Knapsack Solver!")
print ("----------------------------------------------------------------------")

problem = input("Enter \"default\" if you'd like to run algorithm on default "+\
                "problem, \nand other if you'd like to create your own problem: ")
genAlg = None
solution = None

print('\n')

if (problem.lower() == "default"): # default problem
    # initial default boxes for problem
    boxes = []
    boxes.append((20,6))
    boxes.append((30,5))
    boxes.append((60,8))
    boxes.append((90,7))
    boxes.append((50,6))
    boxes.append((70,9))
    boxes.append((30,4))
    boxes.append((30,5))
    boxes.append((70,4))
    boxes.append((20,9))
    boxes.append((20,2))
    boxes.append((60,1))

    # intialize algorithm with problem including boxes and weight limit
    genAlg = GeneticAlgorithm(boxes, 250)
    
else: # custom problem
    print('Instructions: For each box, enter an integer representing weight\n'+\
           'followed by an integer representing importance, seperated'+\
           ' by a comma \n\tFor example: \"1,2\"'+\
           '\n(or \"done\" if there\'s no more boxes).\n\n')

    done = False
    boxesIn = []

    while not done:
        userInput = input('Enter next box weight and importance values '+\
                           '(or \"done\"): ')
        if userInput.lower() == 'done':
            done = True
        else:
            try:
                userInput = tuple(map(int, userInput.split(',')))

                if (len(userInput) != 2 or userInput[0] < 0 or userInput[1] < 0):
                    raise ValueError

                boxesIn.append(userInput)

            except ValueError:
                print ('\n\n\tError: Please give non-negative integers in valid',\
                       'format of \n\ttwo integers seperated by one comma\n',\
                       '\t(or \"done\" if there\'s no more boxes).\n')
        print("")
    
    # get limit for solution
    valid = False
    solutionLimit = 0
    while not valid: # repeat if not given valid parameter
        solutionLimit = input('Please enter the limit weight of your knapsack: ')
        try: # check if is integer
            solutionLimit = int(solutionLimit)
            # check if is positive
            if (solutionLimit <= 0):
                raise ValueError
            valid = True
        except ValueError:
            print("\n\n\tError: Please enter a valid positive integer.\n\n")
    
    # intialize algorithm with problem including boxes and weight limit
    genAlg = GeneticAlgorithm(boxesIn, solutionLimit)
    
    print('\n')
    
# get number of generations to run algorithm for
valid = False
numGenerations = 0
while not valid: # repeat if not given valid parameter
    numGenerations = input('Enter the number of times you\'d '+\
                           'like to run algorithm for: ')
    try: # check if is integer
        numGenerations = int(numGenerations)
        # check if is positive
        if (numGenerations <= 0):
            raise ValueError
        valid = True
    except ValueError:
        print("\n\n\tError: Please enter a valid positive integer.\n\n")

# formatting
print('\n')
print("Searching...")
print ("----------------------------------------------------------------------")
        
# run algorithm
solution = genAlg.run(numGenerations)

# interpret and print solution
if solution is None:
    print("No solution found")
else:
    print("Solution found:", solution)
    print("Weight of solution found:",solution.getPhenotype())
    print("Importance of solution found:",solution.getFitness())

print ("----------------------------------------------------------------------")
print("\nThanks for using Vivian's Knapsack Problem Solver!\n")
print ("----------------------------------------------------------------------")
    