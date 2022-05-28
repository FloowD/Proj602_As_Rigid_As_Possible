import numpy as np
from Edge import *
from scipy.sparse import csgraph
import itertools

class ARAP2:
    def __init__(self, sommets, faces):
        self.sommets = sommets
        self.faces = faces
        self.nbSommets = len(self.sommets)
        
        #On transforme en matrice et liste numpy pour la manipulation
        self.sommetsP = np.array(self.sommets)
        self.sommetsP = np.asmatrix(self.sommetsP)

        # self.sommets2Tri = [[j for j,tri in enumerate(self.faces) if i in tri] for i in range(self.nbSommets)]
        # print(self.sommets2Tri)

        #On crée une matrice qui va stocker les voisins de chaque sommets
        self.voisins = np.zeros((self.nbSommets,self.nbSommets))

        # On récupere les arangements d'une face (cad les sommets voisins)
        listeArangement = map(lambda face: itertools.permutations(face,2), self.faces)
        iterListeArangement = itertools.chain(*listeArangement)
        zipListeArangement = zip(*iterListeArangement)
        #On cast le tous en tuple
        tupleListeArangement = tuple(zipListeArangement)

        self.voisins[tupleListeArangement] = 1

        #On créer une matrice qui va stocker toutes les matrices de rotation pour chaque sommets
        self.rotations = np.zeros((self.nbSommets,3,3))
        #On crée une matrice qui va stocker les poids
        self.poids = np.zeros((self.nbSommets,self.nbSommets), dtype=np.float)
        #On va initialiser le poids
        for sommet in range(self.nbSommets):
            #On récupère les voisins du sommet
            voisins = self.trouverVoisins(sommet)
            for voisin in voisins:
                #On initialise le poids pour chaque voisin du sommet
                self.initPoids(sommet, voisin)

    def trouverVoisins(self, sommet):
        return np.nonzero(self.voisins[sommet]==1)[0]

    def initPoids(self, sommet_i, sommet_j):
        if(self.poids[sommet_i, sommet_j] == 0):
            pointAlpha, pointBeta = self.chercheAlphaBeta(sommet_i,sommet_j)
            edge = Edge(sommet_i, sommet_j)
            poids = edge.calculPoidsArrete(pointAlpha, pointBeta)
        else:
            poids = self.poids[sommet_i, sommet_j]
        self.poids[sommet_i, sommet_j] = poids

    
    def chercheAlphaBeta(self, point1, point2):
        alphaBeta = []
        #Sort les indices qu'on on trouve la valeur
        tab = np.where( (point1 == self.faces) )[0]
        for i in range(len(tab)):
            if(point2 in self.faces[tab[i]]):
                #On affiche la valeur qui n'est pas indicePoint1 et indicePoint2
                face = self.faces[tab[i]]
                alphaBeta.append(face[(face != point1) & (face != point2)][0])

        return alphaBeta
        

    