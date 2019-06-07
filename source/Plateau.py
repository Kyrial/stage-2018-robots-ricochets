#fichier qui contient les fonction pour personnalisé le plateau du jeu
#(par exemple: les disptcher etc...
from tkinter import *
from Case import *

from Interface import *


def dispatcher(nbSortie):

    hauteur=nbSortie*4+3
    largeur= nbSortie + (2*(nbSortie-1))+1




    grille=[[0] * largeur for i in range(hauteur)]
    print(grille)


    
    
    
    ligne= [[ case(gauche=True, droite=True), case(gauche=True, bas=True),case(),case(),case(),case()],
    [ case(),case(haut=True, droite=True) ,case(gauche=True, droite=True),case(gauche=True, droite=True),
      case(gauche=True, droite=True),case(gauche=True, droite=True) ]]

    print(ligne[0][0].__dict__)
    
    #return ligne



    ligneH = [[ case(gauche=True, droite=True),case(gauche=True, droite=True),case(gauche=True, droite=True)
                ,case(gauche=True),case(gauche=True, droite=True),case(gauche=True, droite=True,bas=True)],
              [case(),case(),case(),case(haut=True,bas=True),case(),case()],
              [case(),case(),case(),case(haut=True),case(gauche=True, droite=True),case(gauche=True, droite=True)],
              [case(gauche=True, droite=True), case(gauche=True, bas=True),case(),
               case(haut=True,bas=True),case(),case()],
              [ case(),case(haut=True, droite=True) ,case(gauche=True, droite=True),case( droite=True),
                case(gauche=True, droite=True),case(gauche=True, droite=True, bas = True) ]]

    return ligneH




    #for i in range(6,hauteur,4):
     #   j= 1
      ##  while j < largeur:
        #    while(


x = dispatcher(2)

print(x)

a=interface(Tk())

a.creerCanvas(5,6,x)



print(x[0][0].__dict__)



#on place les murs
for i in range((5) ):
    for j in range(6):
        a.placeMur(x[i][j],i,j)






