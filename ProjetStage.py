from tkinter import *
from random import *

class case:

    ##constructeur
    def __init__ (self, haut, bas, droite, gauche):
        self.haut=haut
        self.bas = bas
        self.droite = droite
        self.gauche = gauche

    ##getter
    def getHaut(self):
        return self.haut



class matrice:
    ##matrice, contient:
        #Les dimensions: L, l
    #une densité de murs
        #nombre de robot: bot
        #nombre de couleur robot: colorR
        #nombre de sortie: exit
        #nombre de couleur sorite: colorE

    ##constructeur
    def __init__(self, longueur, largeur, densite, infoRicochet):
        self.L = longueur
        self.l = largeur

        self.densite = densite
        
        self.bot = infoRicochet[0]
        self.colorR = infoRicochet[1]
        self.exit = infoRicochet[2]
        self.colorE = infoRicochet[3]
        tableau = [[0] * (self.l) for _ in range(self.L)]
        self.tab=tableau

    ##getter
    def getLongueur(self):
        return self.L

    def getLargeur(self):
        return self.l
    def getRobot(self):
        return self.bot
    def getCouleurR(self):
        return self.colorR
    def getSortie(self):
        return self.exit
    def getCouleurE(self):
        return self.colorE

    ##setter
    def setLongueur(self,x):
        self.L=x

    def setLargeur(self,x):
        self.l=x
    def setRobot(self,x):
        self.bot=x
    def setCouleurR(self,x):
        self.colorR=x
    def setSortie(self,x):
        self.exit=x
    def setCouleurE(self,x):
        self.colorE=x


    #cree la matrice par rapport au paramètre.
    #on code l'état une case sur 2
        
    def creerTab(self):

        for i in range((self.L) ):
            print(self.tab[i])
            #for j in range((self.l)):

                #gerer le cas des bordure
                #if(
                





##pour tester:

#nbRobot, nbCouleurRobot, nbSortie, nbcouleurSortie
infoRicochet=[2,2,2,2]

                
tableau=matrice(4,4,4,infoRicochet)


tableau.creerTab()







