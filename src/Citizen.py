import src.Util as Util

class Citizen:
    def __init__(self, masterImage):
        self.masterImage = masterImage        
        self.image = Util.RandomImage(masterImage.shape)
        self.fitness = self.CalculateFitness()

    def CalculateFitness(self):
        h = self.masterImage.shape[0]
        w = self.masterImage.shape[1]
        fitness = 0
        for x in range(0,h):
            for y in range(0,w):
                fitness += Util.PixelDelta(self.image[x][y], self.masterImage[x][y])
        return fitness
