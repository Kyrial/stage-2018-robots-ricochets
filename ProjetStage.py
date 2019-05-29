from tkinter import *
from random import *

class interface:

    def __init__(self, fen ):
        self.fenetre = fen


    def creerCanvas(self, L, l, case):
        self.canvas = Canvas(self.fenetre, width=L*50+50, height=l*50+50,
                             borderwidth=5,background="white")
        self.canvas['scrollregion'] = (-25,-25,L*50+25,l*50+25)

        for li in range(0,L):
            for co in range(0,l):
                Id= self.canvas.create_rectangle(50*li,50*co,50*li+50,50*co+50,
                                        fill='blue', tags= 'carre')
                case[co][li].setId(Id)
                
        
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
       
        identifiant = self.canvas.create_oval((robot.getX()*50)+5,(robot.getY()*50)+5,
                                (robot.getX()*50)+45,(robot.getY()*50)+45,
                                fill=robot.getCouleur(), tags="robot")

        return identifiant



class robot:
    def __init__(self, x, y,couleur):
        self.x=x
        self.y=y
        self.couleur=couleur
        self.Id=0

    ##getter
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getCouleur(self):
        return self.couleur
    def getId(self):
        return self.Id
    ##setter
    def setX(self,a):
        self.x = a
    def setY(self,a):
        self.y = a
    def setCouleur(self,a):
        self.couleur =a
    def setId(self, a):
        self.Id = a

    


class case:

    ##constructeur
    def __init__ (self, haut=False , bas=False, droite=False, gauche=False,
                  alea=False, robot=False, densite=3):

        self.haut = haut
        self.bas = bas
        self.droite = droite
        self.gauche = gauche
        self.robot = robot
        self.Id = 0


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

                #print(self.tab[i][j].__dict__)            
            #print()

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
        self.f.creerCanvas(self.L,self.l, self.tab)

        #on place les murs
        for i in range((self.L) ):
            for j in range(self.l):
                self.f.placeMur(self.tab[i][j],i,j)
                
        #on place les robots
        for i in range(self.getRobot()):            
            Id = self.f.placeRobot(self.tabR[i])

            ##on lie l'Id du cercle au robot
            self.tabR[i].setId(Id)
            


 

    def clique(self,event):
        global selection
        global lastItem
        x = self.f.canvas.canvasx (event.x)
        y = self.f.canvas.canvasy (event.y)
        print(x,"  ", y)
        
        if selection==False:
            lastItem=self.f.canvas.find_closest(x, y,start= "robot")
            print(lastItem)
            print(self.f.canvas.itemcget(lastItem, "tags"))
            if self.f.canvas.itemcget(lastItem, "tags")== "robot current":
                selection=True
                ##ajouter couleur des zones accessibles
                self.afficheMoveCase(True)
                
        else:
            print("coords :",self.f.canvas.coords(lastItem))
            coords = self.f.canvas.coords(lastItem)
            print("x = ", x ," et y = ", y)
            self.afficheMoveCase(False)
            if( coords[0] <= x <=  coords[2]  and y <= coords[1]):                
                self.deplaceH()
            elif( coords[0] <= x <=  coords[2]  and  coords[3] <= y ):               
                self.deplaceB()
            elif( x <=  coords[0]  and  coords[1] <= y <= coords[3]):              
                self.deplaceG()
            elif(   coords[2] <= x  and  coords[1] <= y <= coords[3]):
                self.deplaceD()                

            
            selection = False

               

    def afficheMoveCase(self, boolean):
        global lastItem
        for i in range(self.getRobot()):
            if self.tabR[i].getId() == lastItem[0]:
                x =  self.tabR[i].getX()
                y =  self.tabR[i].getY()
                
                ymin = y - self.movePossibleH(x, y)
                ymax = y + self.movePossibleB(x, y)
                xmin = x - self.movePossibleG(x, y)
                xmax = x + self.movePossibleD(x, y)
                if boolean:
                    for y in range(ymin, ymax+1):
                        self.f.canvas.itemconfigure(self.tab[y][x].getId(),fill="#2e93f9")
                    y =  self.tabR[i].getY()
                    for x in range(xmin, xmax+1):
                        self.f.canvas.itemconfigure(self.tab[y][x].getId(),fill="#2e93f9")
                else:
                    for y in range(ymin, ymax+1):
                        self.f.canvas.itemconfigure(self.tab[y][x].getId(),fill="blue")
                    y =  self.tabR[i].getY()
                    for x in range(xmin, xmax+1):
                        self.f.canvas.itemconfigure(self.tab[y][x].getId(),fill="blue")

                





    def movePossibleH(self, x, y):
        compteur=0       
        while (self.tab[x][y].getHaut() == False and
                self.tab[x][y-1].getBas() == False and
                self.tab[x][y-1].getRobot() == False ):
            y=y-1
            compteur=compteur + 1
        return compteur;


    def movePossibleB(self, x, y):
        compteur=0                    
        while (self.tab[x][y].getBas() == False and
                self.tab[x][y+1].getHaut() == False and
                self.tab[x][y+1].getRobot() == False ):
            y=y+1
            compteur=compteur + 1
        return compteur
    
    def movePossibleG(self, x, y):
        compteur=0                    
        while (self.tab[x][y].getGauche() == False and
                self.tab[x-1][y].getDroite() == False and
                self.tab[x-1][y].getRobot() == False ):
            x=x-1      
            compteur=compteur + 1
        return compteur

 
    def movePossibleD(self, x, y):
        compteur=0
        while (self.tab[x][y].getDroite() == False and
                self.tab[x+1][y].getGauche() == False and
                self.tab[x+1][y].getRobot() == False ):
            x=x+1
            compteur=compteur + 1
        return compteur

   

 
    
    def deplaceH(self):        
        global lastItem
        for i in range(self.getRobot()):
            if self.tabR[i].getId() == lastItem[0]:


                x =  self.tabR[i].getX()
                y =  self.tabR[i].getY()

                compteur = self.movePossibleH(x,y)
                ##si compteur n'est pas nul, le robot a bouge
                if compteur != 0:
                    ##Les informations doivent etre actualise:
                    self.tab[x][y].setRobot( False)
                    y=y-compteur ##actualise y
                    self.tab[x][y].setRobot( True )
                    self.tabR[i].setY(y)
                    ##modif de l'interface graphique:
                    print("x = ", x ," et y = ", y)
                    self.f.canvas.coords(self.tabR[i].getId(),x*50+5,y*50+5,x*50+45,y*50+45)

    def deplaceB(self):        
            global lastItem
            for i in range(self.getRobot()):
                if self.tabR[i].getId() == lastItem[0]:

                    x =  self.tabR[i].getX()
                    y =  self.tabR[i].getY()
                    compteur = self.movePossibleB(x, y)
                    
                    ##si compteur n'est pas nul, le robot a bouge
                    if compteur != 0:
                        ##Les informations doivent etre actualise:
                        self.tab[x][y].setRobot( False)
                        y=y+compteur ##actualise y
                        self.tab[x][y].setRobot( True )
                        self.tabR[i].setY(y)
                        ##modif de l'interface graphique:
                        print("x = ", x ," et y = ", y)
                        self.f.canvas.coords(self.tabR[i].getId(),x*50+5,y*50+5,x*50+45,y*50+45)                
            
    def deplaceG(self):        
            global lastItem
            for i in range(self.getRobot()):
                if self.tabR[i].getId() == lastItem[0]:

                    x =  self.tabR[i].getX()
                    y =  self.tabR[i].getY()
                    compteur=self.movePossibleG(x, y)                    

                    ##si compteur n'est pas nul, le robot a bouge
                    if compteur != 0:
                        ##Les informations doivent etre actualise:
                        self.tab[x][y].setRobot( False)
                        x=x-compteur ##actualise x
                        self.tab[x][y].setRobot( True )
                        self.tabR[i].setX(x)
                        ##modif de l'interface graphique:
                        print("x = ", x ," et y = ", y)
                        self.f.canvas.coords(self.tabR[i].getId(),x*50+5,y*50+5,x*50+45,y*50+45)                
                 
    def deplaceD(self):        
            global lastItem
            for i in range(self.getRobot()):
                if self.tabR[i].getId() == lastItem[0]:

                    x =  self.tabR[i].getX()
                    y =  self.tabR[i].getY()
                    compteur=self.movePossibleD(x, y)
                    
                   ##si compteur n'est pas nul, le robot a bouge
                    if compteur != 0:
                        ##Les informations doivent etre actualise:
                        self.tab[x][y].setRobot( False)
                        x=x+compteur ##actualise x
                        self.tab[x][y].setRobot( True )
                        self.tabR[i].setX(x)
                        ##modif de l'interface graphique:
                        print("x = ", x ," et y = ", y)
                        self.f.canvas.coords(self.tabR[i].getId(),x*50+5,y*50+5,x*50+45,y*50+45)                
                 



##pour tester:

#nbRobot, nbCouleurRobot, nbSortie, nbcouleurSortie
infoRicochet=[2,2,2,2]

                
tableau=matrice(10,10,4,infoRicochet)

#import tkinter.colorchooser
#couleur= tkinter.colorchooser.askcolor()

##savoir si un robot est déjà selectionné
selection= False

##permet de connaitre le dernier robot selectionné
lastItem=0


tableau.f.canvas.focus_set()
tableau.f.canvas.bind("<Button-1>", tableau.clique)

tableau.f.fenetre.mainloop()





