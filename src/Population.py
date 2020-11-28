from src.Citizen import Citizen
from src.Config import Config
from multiprocessing import Pool

import src.Util as Util
import numpy as np
import operator 

class Population:

    def __init__(self, populationSize, masterImage, config = Config(), populate = False):
        self.populationSize = populationSize
        self.masterImage = masterImage
        self.config = config
        self.rankedCitizens = []
        if populate:
            self.Populate()
            self.UpdateRanking()

    def Populate(self):
        print ("Creating population of " + str(self.populationSize) + " citizens.")
        for i in range(0, self.populationSize):
            citizen = Citizen(self.masterImage)
            self.rankedCitizens.append(citizen)

    def ClonePopulation(self, populate = False):
        pop = Population(self.populationSize, self.masterImage, self.config) 
        if populate:
            pop.rankedCitizens = self.rankedCitizens
            pop.fitestCitizen = self.fitestCitizen
        return pop

    def UpdateRanking(self):
        self.rankedCitizens.sort(key=operator.attrgetter("fitness"))
        self.fitestCitizen = self.rankedCitizens[0]
        
    def Evolve(self, generation):
        print ("Evolving: generation " + str(generation))
        pop = self.ClonePopulation()
        offset = 0
        if self.config.elitism:
            elites = self.rankedCitizens[0:self.config.eliteCount+1]
            offset = self.config.eliteCount
            pop.rankedCitizens.extend(elites)
        for x in range(offset, self.populationSize): 
            p1, p2  = self.RouletteSelection()
            child = self.Crossover(p1, p2)
            pop.rankedCitizens.append(child)
        pop.UpdateRanking()
        return pop

    def RouletteSelection(self):
        totalFitness = sum(i.fitness for i in self.rankedCitizens)
        r1 = Util.RandomNumber(0, totalFitness)
        r2 = Util.RandomNumber(0, totalFitness)
        foundP1 = foundP2 = False
        p1 = p2 = None
        i = j = len(self.rankedCitizens) - 1
        while i > 0:
            r1 -= self.rankedCitizens[i].fitness
            if r1 < 0 and foundP1 == False:
                p1 = self.rankedCitizens[i]
                foundP1 = True
            r2 -= self.rankedCitizens[j].fitness
            if r2 < 0 and foundP2 == False:
                p2 = self.rankedCitizens[j]
                foundP2 = True
            if foundP1 and foundP2:
                break;
            i -=1
            j -=1
        if foundP1 and foundP2:
            return p1, p2
        else:     
            return self.rankedCitizens[Util.RandomNumber(0, len(self.rankedCitizens))], self.rankedCitizens[Util.RandomNumber(0, len(self.rankedCitizens))]
            
        
    def Crossover(self, c1, c2):
        h = self.masterImage.shape[0]
        w = self.masterImage.shape[1]
        child = Citizen(self.masterImage)
        shouldMutate = False
        if np.random.uniform(0, 1) > self.config.mutationProbability:
            shouldMutate = True
        for x in range(0,h):
            for y in range(0,w):
                p = self.masterImage[x][y]
                d1 = Util.PixelDelta(p, c1.image[x][y])
                d2 = Util.PixelDelta(p, c2.image[x][y])
                if shouldMutate and np.random.uniform(0, 1) > self.config.mutationProbability:
                    child.image[x][y] = Util.RandomPixel()
                else:
                    if d1<d2:
                        child.image[x][y] = c1.image[x][y]
                    else:
                        child.image[x][y] = c2.image[x][y]
        return child