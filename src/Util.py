import numpy as np
np.seterr(over='ignore')

import math

def RandomImage(shape = (100,100,3)):
        image = np.random.randint(0, 255, size=shape, dtype='uint8')
        return image

def RandomPixel(shape = (1,3)):
        pixel = np.random.randint(0, 255, size=(1, 3), dtype='uint8')
        return pixel

def RandomNumber(start= 0, end = 1):
        num = np.random.randint(start, end)
        return num
        
def PixelDelta(p1, p2):
        r1, g1, b1 = p1
        r2, g2, b2 = p2
        r = r2-r1
        g = g2-g1
        b = b2-b1
        return math.sqrt((r*r) + (g*g) + (b*b))