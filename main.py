#! /usr/bin/python
import numpy as np
from manipModel3D import *
from manipAsRigidAsPossible import *


if __name__ == '__main__':
    sommets, faces = openOffFile('./Data/armadillo_1k.off')
    # print(sommets, faces)

    Arap = ARAP(sommets, faces)
    Arap.genereCellules()
    # print(Arap.sommets)
    print(Arap.tabCellules)

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
Comment on choisi sur quelle partie on effectue la translation ? (Supposition : donner des points qu'on veut qui bouge)
Endroit de départ et endroit d'arrivé ?
Ou juste faire bouger un points n fois ?
!On ne sait pas les nouvelle position

C'est quoi déjà l'énérgie ? Et pourquoi ca aide a transformer ?

"""