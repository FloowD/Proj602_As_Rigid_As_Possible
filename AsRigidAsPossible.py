import numpy as np
from Edge import *
from scipy.sparse import csgraph
import itertools

class ARAP:
    def __init__(self, sommets, faces):
        self.sommets = sommets
        self.faces = faces
        self.nbSommets = len(self.sommets)
        
        #On transforme en matrice et liste numpy pour la manipulation
        self.sommetsPPrime = np.array(self.sommets)
        self.sommetsPPrime = np.asmatrix(self.sommetsPPrime)

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
    """
    Trouve les sommets voisins d'un sommet choisi
    """
    def trouverVoisins(self, sommet):
        return np.where(self.voisins[sommet]==1)[0]
    """
    Initialise le poids pour chaque arrête
    """
    def initPoids(self, sommet_i, sommet_j):
        if(self.poids[sommet_i, sommet_j] == 0):
            pointAlpha, pointBeta = self.chercheAlphaBeta(sommet_i,sommet_j)
            edge = Edge(self.sommets[sommet_i], self.sommets[sommet_j])
            poids = edge.calculPoidsArrete(self.sommets[pointAlpha], self.sommets[pointBeta])
        
        else:
            poids = self.poids[sommet_i, sommet_j]
        self.poids[sommet_i, sommet_j] = poids


    """ 
    Trouve les points apartenant aux triangles n'étant pas les point1 et point2
    """ 
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

    """
    Calcule la matrice P utilisé dans le calcul de la matrice de covariance
    """
    def calcul_P_pour_covariance(self):
        self.tab_P = []
        for sommet_i in range(self.nbSommets):
            pos_sommet_i = np.array(self.sommets[sommet_i])
            voisins = self.trouverVoisins(sommet_i)
            P_i = np.zeros((3, len(voisins)))
            for vi in range(len(voisins)):
                indice_voisin = voisins[vi]
                pos_voisin = np.array(self.sommets[indice_voisin])
                P_i[:, vi] = pos_sommet_i - pos_voisin
            self.tab_P.append(P_i)

    """
    On applique les contraintes au modèle
    """
    def appliquer_contrainte(self, idFixe, idDeplace, matriceDeformation):
        # On utilise la matrice de déformation pour simuler un mouvement
        liste_matrice_deform = list(map(np.matrix, matriceDeformation))

        self.listeSommetDeforme = []
        
        for indice_sommet in range(self.nbSommets):
            if(indice_sommet in idFixe):
                self.listeSommetDeforme.append((indice_sommet, self.sommets[indice_sommet]))

            elif(indice_sommet in idDeplace):
                sommetDeform = np.append(self.sommets[indice_sommet], 1)
                sommetDeform = sommetDeform.dot(liste_matrice_deform[idDeplace.index(indice_sommet)])
                sommetDeform = np.delete(sommetDeform, 3).flatten()
                sommetDeform = np.squeeze(np.asarray(sommetDeform))
                self.listeSommetDeforme.append((indice_sommet, sommetDeform))

        nbSommetDeform = len(self.listeSommetDeforme)

        self.laplacienne = np.zeros((self.nbSommets + nbSommetDeform, self.nbSommets + nbSommetDeform), dtype=np.float32)
        # La matrice poids est une matrice d'adjacence pondéré
        # On la convertit en matrice laplacienne
        self.laplacienne[:self.nbSommets, :self.nbSommets] = csgraph.laplacian(self.poids)

        for i in range(nbSommetDeform):
            sommetCourant = self.listeSommetDeforme[i][0]
            canner = i + self.nbSommets
            self.laplacienne[canner, sommetCourant] = 1
            self.laplacienne[sommetCourant, canner] = 1

        self.b = np.zeros((self.nbSommets + nbSommetDeform, 3))
        for i in range(nbSommetDeform):
            self.b[self.nbSommets + i] = self.listeSommetDeforme[i][1]

        self.calcul_P_pour_covariance()

    """
    Fonction qui applique l'algorithme (calcul des rotations et calcul des p prime)
    """
    def lalgotourne(self, nbIterations):
        for i in range(nbIterations):
            self.calculRotations()
            self.calculPPrime()
    
    """
    Calcule toutes les matrices de rotations
    """
    def calculRotations(self):
        for sommet in range(self.nbSommets):
            matriceRotation = self.calculMatriceRotation(sommet)
            self.rotations[sommet] = matriceRotation

    """
    Calcule la matrice de rotation pour un sommet
    """
    def calculMatriceRotation(self, sommet):
        #On calcul la matrice de covariance
        S = self.calculMatriceCovariance(sommet)
        #On fait la décomposition en valeur singuliere
        U, Sig, V = self.decompositionValeursSinguliere(S)
        #On calcul la matrice de rotation
        R = V.T.dot(U.T)
        # On calcul de determinant de la matrice de rotation pour regarder si il est négatif
        det = np.linalg.det(R)
        if(det < 0):
            # On trouve la valeur minimal de Sig
            indiceMinDiag = np.argmin(Sig)
            # On inverse la colonne dans Ui correspondant à cette valeur minimal
            U[:,indiceMinDiag] = -U[:,indiceMinDiag]
            # On recalcul la matrice de rotation
            R = V.T.dot(U.T)
        
        return R
    """
    Calcul la matrice de covariance pour une cellule
    """
    def calculMatriceCovariance(self, sommet_i):
        sommetPPrime = self.sommetsPPrime[sommet_i]
        voisins = self.trouverVoisins(sommet_i)
        nbVoisins = len(voisins)

        D = np.zeros((nbVoisins, nbVoisins))

        P = self.tab_P[sommet_i]
        P_prime = np.zeros((3, nbVoisins))

        for indiceVoisin in range(nbVoisins):
            sommetVoisin = voisins[indiceVoisin]
            D[indiceVoisin, indiceVoisin] = self.poids[sommet_i, sommetVoisin]
            sommetVoisinPrime = self.sommetsPPrime[sommetVoisin]
            P_prime[:, indiceVoisin] =  sommetPPrime - sommetVoisinPrime

        #On calcul la matrice de covariance
        MatriceCovariance = P.dot(D).dot(P_prime.T)

        return MatriceCovariance

    """
    Applique la décomposition en valeurs singulières
    """
    def decompositionValeursSinguliere(self, S):
        return np.linalg.svd(S)
    
    """
    Calcule les nouveaux sommets après rotation
    """
    def calculPPrime(self):
        for sommet in range(self.nbSommets):
            self.b[sommet] = np.zeros((1, 3))
            voisins = self.trouverVoisins(sommet)
            for voisin in voisins:
                w = self.poids[sommet, voisin] / 2
                r = self.rotations[sommet] + self.rotations[voisin]
                p = np.array(self.sommets[sommet]) - np.array(self.sommets[voisin])
                self.b[sommet] += (w * r.dot(p))
        self.sommetsPPrime = np.linalg.solve(self.laplacienne, self.b)[:self.nbSommets]