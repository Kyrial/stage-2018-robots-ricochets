from tkinter import *
from random import *

class interface:

    def __init__(self, fen ):
        self.fenetre = fen


    def creerCanvas(self, L, l):
        self.canvas = Canvas(self.fenetre, width=L*50+50, height=l*50+50,
                             borderwidth=5,background="white")
        self.canvas['scrollregion'] = (-25,-25,L*50+25,l*50+25)

        for li in range(0,L):
            for co in range(0,l):
                self.canvas.create_rectangle(50*li,50*co,50*li+50,50*co+50,
                                        fill='blue', tags= 'carre')
        
        self.canvas.grid()

    def placeMur(self, cases, x, y):
        if cases.getHaut():
            self.canvas.create_line(x*50   , y*50   , x*50+50 , y*50, width=5)
        if cases.getBas():
            self.canvas.create_line(x*50   , y*50+50, x*50+50 , y*50+50, width=5)
        if cases.getDroite():
            self.canvas.create_line(x*50+50, y*50   , x*50+50 , y*50+50, width=5)
        if cases.getGauche():
            self.canvas.create_line(x*50   , y*50   , x*50    , y*50+50, width=5)

    def placeRobot(self,robot):
       
        self.canvas.create_oval((robot.getX()*50)+5,(robot.getY()*50)+5,
                                (robot.getX()*50)+45,(robot.getY()*50)+45,
                                fill=robot.getCouleur(), tags="robot")



class robot:
    def __init__(self, x, y,couleur):
        self.x=x
        self.y=y
        self.couleur=couleur

    ##getter
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getCouleur(self):
        return self.couleur
    ##setter
    def setX(self,a):
        self.x = a
    def setY(self,a):
        self.y = a
    def setCouleur(self,a):
        self.couleur =a

    
 


class case:

    ##constructeur
    def __init__ (self, haut=False , bas=False, droite=False, gauche=False,
                  alea=False, robot=False, densite=3):

        self.haut = haut
        self.bas = bas
        self.droite = droite
        self.gauche = gauche
        self.robot = robot


        #gère un ou plusieur mur suivant l'aléatoire
      
        if alea:
            while densite >1:
                if randint(0,10) < densite:
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
        self.tabR=[]
        
        self.colorR = infoRicochet[1]
        self.exit = infoRicochet[2]
        self.colorE = infoRicochet[3]
        #tableau = [[0] * (self.l) for _ in range(self.L)]
        self.tab= []
        self.creerTab()

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
            self.tab.append([])
            
            for j in range(self.l):
                
                ##on place des mur aléatoire par rapport a la densite
                self.tab[i].append(case(alea=True, densite= self.densite))

            
                ##on gère le cas des bordures
                if i==0:
                    self.tab[i][j].setGauche(True)
                if i==self.L-1:
                    self.tab[i][j].setDroite(True)
                if j==0:
                    self.tab[i][j].setHaut(True)
                if j==self.l-1:
                    self.tab[i][j].setBas(True)

                print(self.tab[i][j].__dict__)            
            print()

        self.initBot()
        self.creerInterface()


    def initBot(self):
        a=0
        while a < self.getRobot():
        
            x=randint(0,self.L-1)
            y=randint(0,self.l-1)
            if(self.tab[x][y].getRobot()==False):
                self.tabR.append(robot(x, y ,"red"))
                self.tab[x][y].setRobot(True)

                a=a+1
      

    def creerInterface(self):
        self.f=interface(Tk())
        self.f.creerCanvas(self.L,self.l)

        #on place les murs
        for i in range((self.L) ):
            for j in range(self.l):
                self.f.placeMur(self.tab[i][j],i,j)

        #on place les robots
        for i in range(self.getRobot()):
            self.f.placeRobot(self.tabR[i])



 

    def clavier(self,event):
        print("miaou")
            



##pour tester:

#nbRobot, nbCouleurRobot, nbSortie, nbcouleurSortie
infoRicochet=[2,2,2,2]

                
tableau=matrice(8,8,4,infoRicochet)

#import tkinter.colorchooser
#couleur= tkinter.colorchooser.askcolor()



tableau.f.canvas.focus_set()
tableau.f.canvas.bind("<Button-1>", tableau.clavier)

tableau.f.fenetre.mainloop()





