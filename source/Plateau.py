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
    #a=interface(Tk())

    ##on definie la taille du dispatcher suivant le nombre de sortie
    if nbSortie <2:
        hauteur = 7
    else:
        hauteur=floor(log(nbSortie-1,2))*4+7
    largeur=(3*nbSortie)


    ##initialisation du dispatcher
    grille=[[0] * hauteur for i in range(largeur)]
    


    
    
    ##initialisation de la sortie "ligne"
    ligne= [[ case(gauche=True, droite=True), case(gauche=True, bas=True),0,0,0,0,0],
    [ 0,case(haut=True, droite=True) ,case(gauche=True, droite=True),case(gauche=True, droite=True),
      case(gauche=True, droite=True),case(gauche=True, droite=True),case(gauche=True, droite=True) ]]


    
    


    ##initialisation de la double sortie "en H"
    ligneH = [[ case(gauche=True, droite=True),case(gauche=True, droite=True),case(gauche=True, droite=True)
                ,case(gauche=True),case(gauche=True, droite=True),case(gauche=True, droite=True,bas=True),0],
              [0,0,0,case(haut=True,bas=True),0,0,0],
              [0,0,0,case(haut=True),case(gauche=True, droite=True),case(gauche=True, droite=True),case(gauche=True, droite=True)],
              [case(gauche=True, droite=True), case(gauche=True, bas=True),0,
               case(haut=True,bas=True),0,0,0],
              [ 0,case(haut=True, droite=True) ,case(gauche=True, droite=True),case( droite=True),
                case(gauche=True, droite=True),case(gauche=True, droite=True, bas = True),0 ],
              [0,0,0,0,0,0,0]]
              


    ##on plase les sortie sur la grille
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
        distance= 2*x+1
        incremente = x
        ###comme do while n'existe pas en python:
        while True:         
            grille[incremente][y]=case(gauche=True)
            grille[incremente][y+1]=case(gauche=True,droite = True)
            grille[incremente][y+2]=case(gauche=True, droite = True, bas = True)
            
            #besoin d'un booleen pour savoir si le colonne centrale a été placé.
            relier=False
            for trace in range (incremente+1, min((distance)+incremente+1, largeur-2)):
                ##a la moitié on trace l'entrée
                if (trace%(2*(distance+1)) == distance%(2*distance)):
                    relier=True

                    grille[trace][y]=case(haut=True)
                    grille[trace][y+1]=case(gauche=True,droite = True)
                    grille[trace][y+2]=case(gauche=True, droite = True)
                    grille[trace][y+3]=case(gauche=True, droite = True)
                else:
                    grille[trace][y]=case(haut=True, bas = True)
                    

            #s'il n'existe pas deja un chemin:
            if relier:
                grille[min(distance+incremente+1, largeur-2)][y]=case(droite=True)
                grille[min(distance+incremente+1, largeur-2)][y+1]=case(gauche=True,droite = True)
                grille[min(distance+incremente+1, largeur-2)][y+2]=case(gauche=True, droite = True, bas = True)
                #dans le cas ou aucune case n'est au dessus,
                #il suffit de tracer un trait a partir de ce point jusqu'a trouvé une case
                newY=y
                while (grille[min(distance+incremente+1, largeur-2)][newY-1]==0
                       and grille[min(distance+incremente+1, largeur-2)-1][newY-1]==0):
                    grille[min(distance+incremente+1, largeur-2)][newY-1]=case(gauche=True,droite = True)
                    newY=newY-1
                if (grille[min(distance+incremente+1, largeur-2)-1][newY-1]!=0):
                     grille[min(distance+incremente+1, largeur-2)][newY-1]=case(haut=True,droite = True)   



            
            incremente = incremente + 2*(distance+1 )
            
            
            #si on dépasse la taille du dispatcher, on sort le la boucle
            if incremente >= largeur-1:
                break
        x=2*x+1
  


    return grille;


    #print(grille)


##    a.creerCanvas(largeur,hauteur,grille)
##    
##    #on place les murs
##    for i in range(largeur):
##        for j in range(hauteur):
##            if grille[i][j] != 0:
##                a.placeMur(grille[i][j],i,j)


    






a=interface(Tk())

#x = dispatcher(1)      #fonctionne
#x = dispatcher(2)      #fonctionne
#x = dispatcher(3)      #fonctionne
#x = dispatcher(4)      #fonctionne
#x = dispatcher(5)      
#x = dispatcher(6)      
#x = dispatcher(7)      #fonctionne
#x = dispatcher(8)      #fonctionne

#x = dispatcher(9)      
#x = dispatcher(10)     

#x = dispatcher(11)     

#x = dispatcher(12)     

dispatch = dispatcher(20)      
#x = dispatcher(26)      

#fonctionne tous




a.creerCanvas((len(dispatch)),(len(dispatch[0])),dispatch)



#print(x[0][0].__dict__)



###on place les murs
for i in range(len(dispatch) ):
    for j in range(len(dispatch[0])):
        if dispatch[i][j] != 0:
            a.placeMur(dispatch[i][j],i,j)






