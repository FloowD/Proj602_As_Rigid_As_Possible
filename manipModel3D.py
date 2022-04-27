import numpy as np

"""
Cette fonction ouvre une fichier .off et le transforme en matrice de sommets et de faces
"""
# @param path : le chemin vers le fichier .off
def openOffFile(path):
    # On ouvre le fichier donnéé
    fichierOff = open(path, "r")
    # On lit la première ligne pour passer le : OFF
    fichierOff.readline()
    # On lit la deuxieme ligne du fichier off pour récupérer le nombre de sommets, et nombre de faces
    # et on split ces valeurs dans un tableau firstline
    firstLigne = fichierOff.readline().split()
    #On stock le nombre de sommets
    nbSommet = int(firstLigne[0])
    #On stock le nombre de faces (triangulaire)
    nbFaces = int(firstLigne[1])
    
    #On crée une matrice de taille : nombre de faces, 3 colonnes
    # TODO : On pourrait améliorer ce truc, en ne forcant pas 3 colonnes mais en le récupérant
    #?Demander si c'est utile
    sommets = np.zeros((nbSommet, 3))
    #On va parcourir les premières lignes du fichiers qui correspondent aux coordonnées des sommets
    faces = np.zeros((nbFaces, 3), dtype=np.int)
    #On lit la ligne
    for i in range(nbSommet):
        #On stocke les coordonnées dans la matrice sommets
        ligne = fichierOff.readline().split()
        sommets[i, 0] = float(ligne[0])
        sommets[i, 1] = float(ligne[1])
        sommets[i, 2] = float(ligne[2])
    #On fait la même chose pour les faces
    for i in range(nbFaces):
        ligne = fichierOff.readline().split()
        faces[i, 0] = int(ligne[1])
        faces[i, 1] = int(ligne[2])
        faces[i, 2] = int(ligne[3])

    return sommets, faces
    