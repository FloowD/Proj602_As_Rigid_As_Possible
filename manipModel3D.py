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
    

def saveOffFile(sommets, faces, path):
    nouveauFichierOff = open(path, "w")
    # On écrit le : OFF au debut du fichier
    nouveauFichierOff.write('OFF\n')

    # On écrit le nombre de sommets et de faces
    l = []
    l.append(str(len(sommets)))
    l.append(str(len(faces)))
    l.append(str(0))
    nouveauFichierOff.write(' '.join(l)+'\n')

    # On écrit les sommets (les coordonnées)
    for sommet in sommets:
        l = []
        l.append(str(sommet[0]))
        l.append(str(sommet[1]))
        l.append(str(sommet[2]))
        nouveauFichierOff.write(' '.join(l)+'\n')

    # On écrit les faces (les indices des sommets)
    for face in faces:
        l = [str(3)]
        l.append(str(face[0]))
        l.append(str(face[1]))
        l.append(str(face[2]))
        nouveauFichierOff.write(' '.join(l)+'\n')