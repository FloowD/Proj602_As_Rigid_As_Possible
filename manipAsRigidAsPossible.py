import numpy as np
from Edge import *
class ARAP:
    """
    Init pour avoir sommets et faces constaments
    """
    def __init__(self, sommets, faces):
        self.sommets = sommets
        self.faces = faces

    """
    Transforme nos tableaux de sommets et faces en cellules
    """
    def genereCellules(self):
        #!Problème : faire un tableau numpy --> trouver à l'avance le nombre de sommets 
        #Tableau 2D vide avec nbSommets sous tableau
        self.tabCellules = [[] for i in range(len(self.sommets))]
        #On parcourt toutes les surfaces (triangle)
        # print(self.tabCellules
        cpt = 0
        for face in self.faces:
            # if cpt < 2:
                # On parcourt les 3 sommets de la surface (triangle)
            for i in range(0,3):
                # On parcours les sommets de la surface différents de i
                for j in range(0,3):
                    # if(face[i] ==0):
                    #     print(face[j], self.tabCellules[face[i]])
                    #     print((face[j] not in self.tabCellules[face[i]]), (j !=i))
                    if( (face[j] not in self.tabCellules[face[i]]) and (j !=i) ):
                        # print(self.tabCellules[face[i]], self.tabCellules)
                        self.tabCellules[face[i]].append(face[j])

                        
            cpt+=1
    """
    Calcul les poids pour chaque arretes ?
    """  
    def calculPoidsCellules(self):
        #TODO : voir pour le calcul du poids -> normalement on a un poids pour chaque arrete mais on pense que ca fait beaucoup
        """
        Si on veut faire simple on met tous les poids d'arete (w_ij) à 1 --> mais ca donne des résultats mauvais
        Sinon on applique la formule des angles cotangents
        """

        """
        Pour l'instant : 
            On parcrout toutes nos cellules
                dans chaque cellules on calcul le poids de chaque arrete
            Le poids de la cellule devient la somme des poids des arretes qu'elle contient
        """
        #Tableau qui va stocker le poids de toutes les cellules
        self.tabPoidsCellules = [[] for i in range(len(self.sommets))]
        #Stocke le poids de chaque arrete
        self.tabPoidsAretesCellules = [[] for i in range(len(self.sommets))]

        #?On va calculer d'abord le poids de toutes les arretes
        #On parcourt toutes les cellules
        for i, cellule in enumerate(self.tabCellules):
            #On parcourt toutes les arretes de la cellule
            for j in cellule:
                #On récupère les 2 autres sommets pour le calcul du poids
                pointAlpha, pointBeta = self.chercheFaces(i,j)
                #On créer un sommet entre les 2 points courant
                edge = Edge(self.sommets[i], self.sommets[j])
                #On calcul le poids de l'arrete
                poidsArrete = edge.calculPoidsArrete(pointAlpha, pointBeta)
                #On stocke le poids de l'arrete
                self.tabPoidsAretesCellules[i].append(poidsArrete)
            
            #On calcule le poids de la cellule
            self.tabPoidsCellules[i] = sum(self.tabPoidsAretesCellules[i])
        

                
                
    
    
    """
    Fonction qui va retourner les 2 faces (triangle), qui contiennent les 2 points
    """
    #TODO : a modifier ou supprimer pour trouver les bon sommets
    def chercheFaces(self, point1, point2):
        face_correcte = []
        # indicePoint1 = self.getIndiceSommet(point1)
        # indicePoint2 = self.getIndiceSommet(point2)
        #On parcourt toutes les faces
        for face in self.faces:
            #On regarde si les 2 points sont dans la face courante
            if(point1 in face and point2 in face):
                #Si oui on ajoute le point qui n'est n'y indicePoint1 et indicesPoint2
                face_correcte.append(face[face != point1][0])
        return face_correcte

    """
    Donne l'indice du sommet par rapport à la liste de sommets
    """
    def getIndiceSommet(self, sommet):
        res = np.where(self.sommets == sommet)
        return res[0][0]
    
    """
    Fonction qui va initaliser la matrice rotation
    """
    def initMatriceRotation(self):
        #On initialise la matrice rotation
        self.R = np.identity(len(self.sommets))

    """
    Calcul la matrice de rotation pour une cellule (la ième cellule)
    """
    def calculMatriceRotation(self, i):
        #On calcul la matrice de covariance
        S = self.calculMatriceCovariance(i)
        #On fait la décomposition en valeur singuliere
        U, Sig, V = self.decompositionValeursSinguliere(S)
        
        return np.dot(V,U.T)

    """
    Applique la décomposition en valeurs singulière pour une matrice 
    """
    def decompositionValeursSinguliere(self, S):
        return np.linalg.svd(S)

    
    """
    Calcul la matrice de covariance pour une cellule
    """
    def calculMatriceCovariance(self, i):
        #On calcul D
        D = np.zeros((len(self.tabPoidsCellules), len(self.tabPoidsCellules)))
        np.fill_diagonal(D, self.tabPoidsCellules)

        #On calcul P -> e_i,j
        P = np.zeros((3, len(self.tabPoidsCellules[i])))
        P_p = np.zeros((3, len(self.tabPoidsCellules[i])))
        cellule = self.tabCellules[i]
        for index, j in enumerate(cellule):
            e_ij = self.sommets[i] - self.sommets[j]
            e_ij_p = self.R*e_ij
            P[:,index] = e_ij
            P_p[:,index] = e_ij_p

        #On calcul la matrice de covariance
        MatriceCovariance = np.dot(P, np.dot(D, P_p.T))

        return MatriceCovariance

