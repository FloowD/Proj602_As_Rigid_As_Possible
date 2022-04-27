import numpy as np

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
            
