import numpy as np
from Edge import *
from scipy.sparse import csgraph
import itertools

class ARAP2:
    def __init__(self, sommets, faces):
        #On stocke la matrice des sommets
        self.sommets = sommets
        #On stocke la matrice faces (qui sont des triangles)
        self.faces = faces
        #On stocke le nombre de sommets
        self.nbSommets = len(self.sommets)
        #On stocka les sommets P (ceux qu'on va modifier)
        self.sommetsP = np.array(self.sommets)
        #On transforme le tableau en matrice pour la manipulation
        self.sommetsP = np.asmatrix(self.sommetsP)

        self.sommets2Tri = [[j for j,tri in enumerate(self.faces) if i in tri] for i in range(self.nbSommets)]
        #On crée une matrice qui va stocker les voisins de chaque sommets
        self.voisins = np.zeros((self.nbSommets,self.nbSommets))
        #On modifie les valeurs dans la matrice des voisins
        self.voisins[
            tuple(zip(
                *itertools.chain(
                    *map(
                        lambda tri: itertools.permutations(tri,2),
                        self.faces
                    )
                )
            ))]=1

        #On créer une matrice qui va stocker toutes les matrices de rotation pour chaque sommets
        self.rotations = np.zeros((self.nbSommets,3,3))
        #On crée une matrice qui va stocker les poids
