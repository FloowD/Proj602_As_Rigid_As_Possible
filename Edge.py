import numpy as np
from math import acos
from mpmath import cot

class Edge:
    
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.weight = 1

    """
    Calcule le poids de l'arrete
    """
    def calculPoidsArrete(self, pointAlpha, pointBeta):
        angleAlpha = self.calculAngle(self.i, pointAlpha, self.j)
        angleBeta = self.calculAngle(self.i, pointBeta, self.j)

        return (cot(angleAlpha) + cot(angleBeta)) / 2



    def calculAngle(self, point1, point2, point3):
        vectPoint2Point1 = point2 - point1
        vectPoint2Point3 = point2 - point3
        produitScalaire = np.dot(vectPoint2Point1, vectPoint2Point3)
        normePoint2Point1 = np.linalg.norm(vectPoint2Point1)
        normePoint2Point3 = np.linalg.norm(vectPoint2Point3)
        angle = produitScalaire / (normePoint2Point1 * normePoint2Point3)
        return acos(angle)
    