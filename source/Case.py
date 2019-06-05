#####CLASS CASE#####
from random import *


class case:

    ##constructeur
    def __init__ (self, haut=False , bas=False, droite=False, gauche=False,
                  alea=False, robot=False, sortie = False, densite=3):

        self.haut = haut
        self.bas = bas
        self.droite = droite
        self.gauche = gauche
        self.robot = robot
        self.sortie = sortie
        self.Id = 0


        #gère un ou plusieur mur suivant l'aléatoire
      
        if alea:
            while densite >10:
                if randint(0,100) < densite:
                    self.ajoutAleatMur()
                densite=densite/2-1


    ##getter
    def getHaut(self):
        return self.haut
    def getBas(self):
        return self.bas
    def getDroite(self):
        return self.droite
    def getGauche(self):
        return self.gauche
    def getRobot(self):
        return self.robot
    def getSortie(self):
        return self.sortie
    def getId(self):
        return self.Id

    ##setter
    def setHaut(self, x):
        self.haut= x
    def setBas(self, x):
        self.bas = x
    def setDroite(self, x):
        self.droite = x
    def setGauche(self, x):
        self.gauche = x
    def setRobot(self, x):
        self.robot = x
    def setSortie(self, x):
        self.sortie = x
    def setId(self, a):
        self.Id = a

    ##genere mur aléatoire
    def ajoutAleatMur(self):
        alea=randint(1,4)
        if alea ==1:
            self.haut = True
        elif alea ==2:
            self.bas = True
        elif alea ==3:
            self.droite = True
        elif alea ==4:
            self.gauche = True
        
