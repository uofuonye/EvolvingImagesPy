from src.Population import Population
from src.Config import Config
from cv2 import cv2

def main(): 
    try: 
        config = Config(elitism= True, eliteCount=2, mutationProbability= 0.1)
        masterImage = cv2.imread("images/facebook.jpg") 
        masterImage = cv2.resize(masterImage,(10,10))
        cv2.imwrite('images/output/master.jpg', masterImage)
        population = Population(populationSize = 50, masterImage = masterImage, config=config, populate=True)
        originalFitness = population.fitestCitizen.fitness
        generation = 0
        Max_Generation = 100000000
        while generation< Max_Generation:
            population = population.Evolve(generation)
            fitestCitizen = population.fitestCitizen
            fitnessPercentage = 100 * (originalFitness - fitestCitizen.fitness)/originalFitness
            print("Fitness = " + str(fitestCitizen.fitness) + " : FitnessPercentage = " + str(fitnessPercentage) + "%")
            if generation % 1000 == 0:
                cv2.imwrite('images/output/generation' + str(generation) + ".jpg", fitestCitizen.image)
            generation += 1
    except IOError: 
        pass
  


if __name__ == "__main__": 
    main() 