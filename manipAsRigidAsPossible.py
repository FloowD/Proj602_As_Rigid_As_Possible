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
            
            #On fixe le poids de la cellule à 1
            self.tabPoidsCellules[i] = 1
        

                
                
    
    
    """
    Fonction qui va retourner les 2 faces (triangle), qui contiennent les 2 points
    """
    def chercheFaces(self, point1, point2):
        face_correcte = []
        # indicePoint1 = self.getIndiceSommet(point1)
        # indicePoint2 = self.getIndiceSommet(point2)
        #Sort les indices qu'on on trouve la valeur
        tab = np.where( (point1 == self.faces) )[0]
        for i in range(len(tab)):
            if(point2 in self.faces[tab[i]]):
                #On affiche la valeur qui n'est pas indicePoint1 et indicePoint2
                face = self.faces[tab[i]]
                face_correcte.append(face[(face != point1) & (face != point2)][0])

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
        self.R = np.identity(len(self.tabCellules[0]))

    """
    Calcul la matrice de rotation pour une cellule (la ième cellule)
    """
    def calculMatriceRotation(self, i):
        #On calcul la matrice de covariance
        S = self.calculMatriceCovariance(i)
        #On fait la décomposition en valeur singuliere
        U, Sig, V = self.decompositionValeursSinguliere(S)

        #On calcul la matrice de rotation
        R = np.dot(V, U.T)

        # On calcul de determinant de la matrice de rotation pour regarder si il est négatif
        det = np.linalg.det(R)
        if(det < 0):
            # On trouve la valeur minimal de Sig
            indiceMinDiag = np.argmin(np.diagonal(Sig))
            # On inverse la colonne dans Ui correspondant à cette valeur minimal
            U[:,indiceMinDiag] = -U[:,indiceMinDiag]
            # On recalcul la matrice de rotation
            R = np.dot(V, U.T)
            # print(indiceMinDiag)
        
        print(R)
        
        return R

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
        cellule = self.tabCellules[i]
        P = np.zeros((3, len(cellule)))
        P_p = np.zeros((3, len(cellule)))
        for index, j in enumerate(cellule):
            e_ij = self.sommets[i] - self.sommets[j]
            print(e_ij, self.R)
            e_ij_p = self.R*e_ij
            P[:,index] = e_ij
            P_p[:,index] = e_ij_p

        #On calcul la matrice de covariance
        MatriceCovariance = np.dot(P, np.dot(D, P_p.T))

        return MatriceCovariance

    """
    Calcul la vecteur b pour le calcul des p'
    """
    def trouver_b(self):
        self.b = np.zeros((len(self.tabCellules), 1))
        for index_i, i in enumerate(self.tabCellules):
            for index_j, j in enumerate(i):
                Ri = self.calculMatriceRotation(i)
                Rj = self.calculMatriceRotation(j)
                wij = self.tabPoidsAretesCellules[index_i][index_j]
                pi = self.sommets[i]
                pj = self.sommets[j]
                self.b[index_i] += (wij/2)*(Ri + Rj) * (pi - pj)

    """
    Calcul les p'
    """
    #!On fait la version 'simple' pour tester
    def trouverPPrime(self):
        self.pPrime = np.zeros((len(self.sommets), 3))
        #On va parcourrir la cellule
        for index_i, i in enumerate(self.tabCellules):
            ...


    """
    Calcul Laplacien
    """
    def calculLaplacien(self):
        self.L = np.zeros((len(self.tabCellules), len(self.tabCellules)))
        for index_i, i in enumerate(self.tabCellules):
            somme_poids = 0
            for index_j, j in enumerate(i):
                somme_poids += self.tabPoidsAretesCellules[index_i][index_j]
                self.L[index_i][index_j] = self.tabPoidsAretesCellules[index_i][index_j]
            self.L[index_i, index_i] = -somme_poids

        

    def appliquerContraintesLaplacien(self, tabContraintes):
        for indice_sommet_contraint in tabContraintes:
            #On met toutes les valeurs de la ligne à 0
            self.L[indice_sommet_contraint] = np.zeros((len(self.tabCellules), 1))
            #On met 1 dans la diagonale
            self.L[indice_sommet_contraint, indice_sommet_contraint] = 1
            # p'j = ck
            self.b[indice_sommet_contraint] = self.sommets[indice_sommet_contraint]
            
            #On met les valeurs dans la colonne de l'indice à 0
            for index_i, i in enumerate(self.tabCellules):
                if(indice_sommet_contraint in i):
                    val = self.L[index_i][indice_sommet_contraint]
                    self.L[index_i][indice_sommet_contraint] = 0
                    #On met dans b la nouvelle valeur
                    self.b[index_i] = self.b[index_i] - val*self.sommets[indice_sommet_contraint]
                
                




