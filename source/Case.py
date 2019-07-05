#####CLASS CASE#####
from random import *


class case:

    ##constructeur
    def __init__ (self, haut=False , bas=False, droite=False, gauche=False,
                  alea=False, robot=False, sortie = False, densite=30):

        self.haut = haut
        self.bas = bas
        self.droite = droite
        self.gauche = gauche
        self.robot = robot
        self.sortie = sortie
        self.Id = 0
        self.exterieur = False


        #gère un ou plusieur mur suivant l'aléatoire
      
        if alea:
            nbMur = 2
            while nbMur > 0:
                
                if randint(0,100) < densite:
                    self.ajoutAleatMur()
                    nbMur= nbMur-1
                else:
                    nbMur = 0
                


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

    def sumMur(self):
        return( (1 if self.bas else 0)+(1 if self.haut else 0)+
                (1 if self.droite else 0)+(1 if self.gauche else 0))

    def getExterieur(self):
        return self.exterieur

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
    def setExterieur(self,a):
        self.exterieur= a

    ##genere mur aléatoire
    def ajoutAleatMur(self):
        alea=randint(1,2)
        if alea ==1:
            self.bas = True
        elif alea ==2:
            self.droite = True


    

###FIN CASE###



        
