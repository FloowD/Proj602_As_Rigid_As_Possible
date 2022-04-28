#! /usr/bin/python
import numpy as np
from manipModel3D import *
from manipAsRigidAsPossible import *
import polyscope as ps

if __name__ == '__main__':
    sommets, faces = openOffFile('./Data/armadillo_1k.off')
    sommets2, faces2 = openOffFile('./Data/dino.off')
    # print(sommets, faces)

    Arap = ARAP(sommets, faces)
    Arap.genereCellules()
    # print(Arap.sommets)
    print(Arap.tabCellules)
    ps.init()
    ps.register_surface_mesh("my mesh", sommets, faces, smooth_shade=True)
    ps.register_surface_mesh("my mesh2", sommets2, faces2, smooth_shade=True)
    ps.show()

"""
Les questions qu'on se pose :

- Comment on définie les cellules du modèle ? -> Comment on les choisis ?
==> Elles doivent avoir une surface similaire et la superposition doit etre choisi par le fait que 'chaque surface est couverte par le meme nombre de cellues' -> pas compris
I - paragraphe 4

Idée de solution : de même taille et ca dépend du nombre de points

?Solution : 
On va parcourir toutes les surfaces (triangle)
    On parcourt les sommets de la surface (i)
        On parcourt les sommets de la surfaces (j)
            Si j n'est pas dans le tableau de cellues[i] et j != i
                tableau de cellues [i] .append(j)


!Problème :
Comment on sait à l'avance le nombre de points pour définir une cellules ? --> Normalement, le meme nombre pour chaque cellule

Une fois qu'on a les cellules --> trouver les voisins ? combien on en prends ?


?Ce qu'on a compris :
    Appliquer la translation sur les cellules en appliquant une formule 

?Ce qu'on a pas compris :
Comment on calcule le poids d'une cellule ?
Demander d'expliquer la formule de calcul du poids d'une cellule
Comment on choisi sur quelle partie on effectue la translation ? (Supposition : donner des points qu'on veut qui bouge)
Endroit de départ et endroit d'arrivé ?
Ou juste faire bouger un points n fois ?
!On ne sait pas les nouvelle position

Faut il appliquer des contraintes sur la model 3D (bloquer les pates du dino)

C'est quoi déjà l'énérgie ? Et pourquoi ca aide a transformer ?


Explication sur le poids: 
lié a l'opérateur Laplacien triangle sur la surface

Trouver R : décomposition en valeur singulière, dans les 3 matrices de sortie on en garde 2 -> puis petit calcul et c'est bon
a la fin du calcul -> determinant --> si négatif -> on inverse les valeurs de la colonne des Ui (regarder la colonne où on a la plus petite valeur)

!Étape de l'algo en entier
- Créer les cellules
- Calculer l'énergie pour chaque cellule
    On applique la formule :
    Dans 1 cellule : applique la formule dans le 2.1 (3)
    Pour toutes les cellules : applique la formule dans le 2.2 (7)
    ?Demander la différence entre le w_(i) et w_(i,j)

--> Trouver les paramètres de R pour minimiser l'énergie

L'énergie sert à :
    - Trouver les positions p' en minimisant l'énergie
    - Trouver la rotation en minimisant l'énergie

- Calculer la rotation pour chaque cellule afin de minimiser l'énérgie
    Demander d'expliquer la formule pour le calcul de la rotation

"""


"""
Récap des informations :

!Étape du programme 
    - Calcul des cellules (déjà codé)
    - Calcul du poids de chaque cellules (appliquer la formule du poids) cot = cotangente
        ?Demander la différence entre le w_(i) et w_(i,j)
    - Initialise la matrice de Rotation à une matrice Identité
    - Méthode pour calculer la nouvelle matrice de rotation
        ---> Décomposition en valeur singulière de Si (voir formule (5))
        Sur les 3 matrices en sorties, on garde la première et la dernière
        a la fin du calcul -> determinant --> si négatif -> on inverse les valeurs de la colonne des Ui (regarder la colonne où on a la plus petite valeur dans la diagonale)
    - Méthode pour calculer les p'
        ---> Appliquer la formule de calcul sur chaque ligne (voir formule (8))
        Faire la formule (9) pour résoudre le tous
            ?Demander a Collin pour être sur

    On doit faire le tous (calcul rotation et p') tant que l'énergie minimal n'est pas atteinte (formule (7))


"""