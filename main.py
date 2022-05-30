#! /usr/bin/python
import numpy as np
from manipModel3D import *
from AsRigidAsPossible import *
import polyscope as ps

if __name__ == '__main__':

    # MODIFIER ICI POUR LE CHOIX DU FICHIER .off
    # structure = 'armadillo_1k'
    # structure = 'bar1'
    structure = 'cactus_small'
    # structure = 'cactus_highres'

    # On récupère les données de la structure
    sommets, faces = openOffFile('./Data/'+structure+'.off')
    
    # On initialise la déformation as rigid as possible (on trouve les cellules/voisins, on initialise les poids, etc.)
    Arap = ARAP(sommets, faces)

    # MODIFIER ICI POUR LE CHOIX DES POINTS FIXES ET DEPLACES
    # On applique des contraintes sur le modèle
    # Démo tatou pour le fichier 'armadillo_1k' :
    Arap.appliquer_contrainte([], range(200,203), np.stack([np.random.rand(4,4)]*3))
    # Démo pour le fichier 'bar1.off'
    #Arap.appliquer_contrainte([], range(90,93), np.stack([np.random.rand(4,4)]*3))
    # Démo pour le fichier 'cactus_small.off'
    # Arap.appliquer_contrainte([],range(177, 180), np.stack([np.random.rand(4,4)]*3))
    
    # On applique l'algorithme avec un nombre d'itérations fixé
    Arap.lalgotourne(100)
    # On sauvegarde le résultat
    saveOffFile(Arap.sommetsPPrime, faces, './Data/deformed_' + structure + '.off')
    # On affiche les 2 modèles avec polyscope
    ps.init()
    ps.register_surface_mesh("my mesh", sommets, faces, smooth_shade=False)
    ps.register_surface_mesh("my mesh deformed", Arap.sommetsPPrime, faces, smooth_shade=False)
    ps.show()
