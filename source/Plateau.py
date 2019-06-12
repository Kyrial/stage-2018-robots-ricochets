#fichier qui contient les fonction pour personnalisé le plateau du jeu
#(par exemple: les disptcher etc...
from tkinter import *
from math import*

from Case import *

from Interface import *


def copieTab(grille, extrait, x, y ):
    for i in range(len(extrait)):
        for j in range(len(extrait[0])):
            grille[x+i][y+j]=extrait[i][j]




def dispatcher(nbSortie):
    global a

    hauteur=floor(log(nbSortie,2))*4+7
    largeur=(3*nbSortie)




    grille=[[0] * hauteur for i in range(largeur)]
    #print(grille)


    
    
    
    ligne= [[ case(gauche=True, droite=True), case(gauche=True, bas=True),0,0,0,0,0],
    [ 0,case(haut=True, droite=True) ,case(gauche=True, droite=True),case(gauche=True, droite=True),
      case(gauche=True, droite=True),case(gauche=True, droite=True),case(gauche=True, droite=True) ]]

    print(ligne[0][0].__dict__)
    
    



    ligneH = [[ case(gauche=True, droite=True),case(gauche=True, droite=True),case(gauche=True, droite=True)
                ,case(gauche=True),case(gauche=True, droite=True),case(gauche=True, droite=True,bas=True),0],
              [0,0,0,case(haut=True,bas=True),0,0,0],
              [0,0,0,case(haut=True),case(gauche=True, droite=True),case(gauche=True, droite=True),case(gauche=True, droite=True)],
              [case(gauche=True, droite=True), case(gauche=True, bas=True),0,
               case(haut=True,bas=True),0,0,0],
              [ 0,case(haut=True, droite=True) ,case(gauche=True, droite=True),case( droite=True),
                case(gauche=True, droite=True),case(gauche=True, droite=True, bas = True),0 ],
              [0,0,0,0,0,0,0]]
              

   #return ligneH

    compteur = 0
    while compteur < nbSortie:
        if compteur <=nbSortie-2:
            copieTab(grille, ligneH, compteur*3, 0)
            compteur = compteur +2
        else:
            copieTab(grille, ligne, (compteur)*3, 0)
            compteur = compteur +1

    
    ##on doit maintenant relier les sorties
    x=2
    for y in range(7,hauteur, 4):
        #distance= 2*x+1
        #incremente = x
        #comme do while n'existe pas en python:
        #while True:
        
            incremente = x
            distance= 2*x+1
          
            grille[incremente][y]=case(gauche=True)
            grille[incremente][y+1]=case(gauche=True,droite = True)
            grille[incremente][y+2]=case(gauche=True, droite = True, bas = True)
 
            for trace in range (incremente+1, min((distance)+incremente+1, largeur-2)):
                if trace == min( largeur-2, distance):
                    grille[trace][y]=case(haut=True)
                    grille[trace][y+1]=case(gauche=True,droite = True)
                    grille[trace][y+2]=case(gauche=True, droite = True)
                    grille[trace][y+3]=case(gauche=True, droite = True)

                else:
                    grille[trace][y]=case(haut=True, bas = True)

            
            grille[min(distance+x+1, largeur-2)][y]=case(droite=True)
            grille[min(distance+x+1, largeur-2)][y+1]=case(gauche=True,droite = True)
            grille[min(distance+x+1, largeur-2)][y+2]=case(gauche=True, droite = True, bas = True)
            
            x=2*x+1

            #if incremente+distance >= largeur:
                #break

    





    #print(grille)


    a.creerCanvas(largeur,hauteur,grille)
    
    #on place les murs
    for i in range(largeur):
        for j in range(hauteur):
            if grille[i][j] != 0:
                a.placeMur(grille[i][j],i,j)








print(floor(log(6,2)))

a=interface(Tk())
x = dispatcher(12)

#print(x)



#a.creerCanvas(6,7,x)



#print(x[0][0].__dict__)



#on place les murs
#for i in range((6) ):
 #   for j in range(7):
  #      if x[i][j] != 0:
   #         a.placeMur(x[i][j],i,j)






