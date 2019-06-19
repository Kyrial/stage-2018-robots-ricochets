from tkinter import *
import random

import sys, os, platform

##messagebox:
from tkinter.messagebox import *
from tkinter.simpledialog import askinteger

##ppour ouvrir la fenetre de recherche de fichier
from tkinter.filedialog import *

#import Plateau

#on importe les autres classes: case, robot, sortie, interface
from Case import *
from Robot import *
from Sortie import *
from Interface import *


##le fichier Matrice fais office de fichier principale, c'est celui
##qui sera executé pour lancer l'application.





#####CLASS MATRICE#####
##La classe matrice servira à gerer la grille du jeu



class matrice:
    ##matrice, contient:
        #Les dimensions: L, l
    #une densité de murs
        #nombre de robot: bot
        #nombre de couleur robot: colorR
        #nombre de sortie: exit
        #nombre de couleur sortie: colorE
    #tableau contenant les robots: tabR
    #tableau contenant la grille: tab
    #tableau contenant les sortie: tabS
    #tableau contenant toute les couleurs utilisé: tabCouleur

    ##constructeur
    def __init__(self, longueur=10, largeur=10, densite=60, infoRicochet=[2,2,2,2],
                 solvable = False,mouvement=10, fichier= None,edition=False):

        ##on lie l'interface a l'objet
        global f
        self.f=f
        

        #tableau de robots
        self.tabR=[]

        #la matrice
        self.tab= []

        #tableau des sorties
        self.tabS = []

        #tableau des différentes couleur utilisé
        self.tabCouleur = []

        self.reinitialise()

        if edition:
            self.editeur()

        
        elif fichier ==None:

            self.L = longueur
            self.l = largeur

            self.densite = densite
            self.solvable= solvable
            self.mouvement=mouvement
            
            self.bot = infoRicochet[0]

            
            self.colorR = infoRicochet[1]
            self.exit = infoRicochet[2]
            self.colorE = infoRicochet[3]
            self.creerTab()

        else:
            print(fichier)
            self.fichier = fichier
            self.creerViaFichier()
            

        
     

    def reinitialise(self):
        global selection, lastItem, move, gagner, pause
        selection= False
        lastItem=[0]
        move=0
        gagner=False
        pause=False

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


    def ajoutBordure(self):
        for i in range((self.L) ):
            for j in range(self.l):             
                ##on ajoute un mur aux bordures de la grille par sécurité
                if i==0:
                    self.tab[i][j].setGauche(True)
                if i==self.L-1:
                    self.tab[i][j].setDroite(True)
                if j==0:
                    self.tab[i][j].setHaut(True)
                if j==self.l-1:
                    self.tab[i][j].setBas(True)


####pour l'editeur:

    def changeCase(self,event):
        
        x = self.f.canvas.canvasx (event.x)
        y = self.f.canvas.canvasy (event.y)
        


        x=int(x//self.f.tailleCase)
        y=int(y//self.f.tailleCase)

        ##pour que les coordonnée soit au centre de la case
        ##et pour que dans les cas le robot/sortie soit selectionnée
        item=self.f.canvas.find_closest(int(x*self.f.tailleCase+(self.f.tailleCase/2)),
                                        int(y*self.f.tailleCase+(self.f.tailleCase/2)))
        
        print(x,"  ", y)
        if self.f.caseCocher.get() == "haut":
            if self.tab[x][y].getHaut()==True:
                self.tab[x][y].setHaut(False)
                self.f.canvas.delete(str(self.tab[x][y].getId())+"h")
            else:   
                self.tab[x][y].setHaut(True)
                self.f.placeMur(self.tab[x][y],x,y)
                
        if self.f.caseCocher.get() == "bas":
            if self.tab[x][y].getBas()==True:
                self.tab[x][y].setBas(False)
                self.f.canvas.delete(str(self.tab[x][y].getId())+"b")
            else:   
                self.tab[x][y].setBas(True)
                self.f.placeMur(self.tab[x][y],x,y)
                
        if self.f.caseCocher.get() == "droite":
            if self.tab[x][y].getDroite()==True:
                self.tab[x][y].setDroite(False)
                self.f.canvas.delete(str(self.tab[x][y].getId())+"d")
            else:   
                self.tab[x][y].setDroite(True)
                self.f.placeMur(self.tab[x][y],x,y)
                
        if self.f.caseCocher.get() == "gauche":
            if self.tab[x][y].getGauche()==True:
                self.tab[x][y].setGauche(False)
                self.f.canvas.delete(str(self.tab[x][y].getId())+"g")
            else:   
                self.tab[x][y].setGauche(True)
                self.f.placeMur(self.tab[x][y],x,y)

        if self.f.caseCocher.get() == "robot":
            if self.tab[x][y].getRobot()==True:
               
                self.tab[x][y].setRobot(False)
                for i in range(len(self.tabR)):
                    if self.tabR[i].getId() == item[0]:
                        self.f.canvas.delete(item[0])
                        
                        del self.tabR[i]
                        self.bot = self.bot-1
                        
                        break
                                
                #self.f.canvas.delete(str(self.tab[x][y].getId())+"g")
            elif(self.tab[x][y].getSortie()==False and
                 self.tab[x][y].getRobot()==False):
                
                self.tab[x][y].setRobot(True)
                self.couleurPipette=self.genererCouleur()
                self.tabR.append(robot(x,y,self.couleurPipette))
                Id=self.f.placeRobot(self.tabR[-1])
                self.tabR[-1].setId(Id)
                self.bot = self.bot+1


        if self.f.caseCocher.get() == "sortie":
            if self.tab[x][y].getSortie()==True:
               
                self.tab[x][y].setSortie(False)
                for i in range(len(self.tabS)):
                    if self.tabS[i].getId() == item[0]:
                        self.f.canvas.delete(item[0])
                        
                        del self.tabS[i]
                        self.exit =self.exit -1
                        
                        break
                                
                #self.f.canvas.delete(str(self.tab[x][y].getId())+"g")
            elif(self.tab[x][y].getSortie()==False and
                 self.tab[x][y].getRobot()==False):
                
                self.tab[x][y].setSortie(True)
                self.couleurPipette=self.genererCouleur()
                self.tabS.append(sortie(x,y,self.couleurPipette))
                Id=self.f.placeSortie(self.tabS[-1])
                self.tabS[-1].setId(Id)
                self.exit = self.exit+1


    def cliqueDroit(self,event):
        x = self.f.canvas.canvasx (event.x)
        y = self.f.canvas.canvasy (event.y)
        
        x=int(x//self.f.tailleCase)
        y=int(y//self.f.tailleCase)

        item=self.f.canvas.find_closest(int(x*self.f.tailleCase+(self.f.tailleCase/2)),
                                        int(y*self.f.tailleCase+(self.f.tailleCase/2)))

        if self.tab[x][y].getSortie()==True:

            for i in range(len(self.tabS)):
                if self.tabS[i].getId() == item[0]:

                    self.couleurPipette = self.tabS[i].getCouleur()
                    break
                
        if self.tab[x][y].getRobot()==True:
        
            for i in range(len(self.tabR)):
                if self.tabR[i].getId() == item[0]:

                    self.couleurPipette = self.tabR[i].getCouleur()
                    break




        if self.f.caseCocher.get() == "robot":


            if (self.tab[x][y].getSortie()==False and
                 self.tab[x][y].getRobot()==False):
                self.tab[x][y].setRobot(True)
                self.tabR.append(robot(x,y,self.couleurPipette))
                Id=self.f.placeRobot(self.tabR[-1])
                self.tabR[-1].setId(Id)
                self.bot = self.bot+1
                
        if self.f.caseCocher.get() == "sortie":

            if (self.tab[x][y].getSortie()==False and
                 self.tab[x][y].getRobot()==False):  
                self.tab[x][y].setSortie(True)
                self.tabS.append(sortie(x,y,self.couleurPipette))
                Id=self.f.placeSortie(self.tabS[-1])
                self.tabS[-1].setId(Id)
                self.exit = self.exit+1


##    def rouletteUp(self,event=None):
##        #aggrendit d'une case la matrice
##        print("miaou")
##        self.L = self.L+1
##        
##            
##        for i in range(self.l):               
##            self.tab[i].append(case())
##
##        self.l = self.l+1
##
##        self.tab.append([])
##        for j in range (self.L):
##            self.tab[self.L-1].append(case())
##
##
##        self.f.canvas.destroy() 
##        self.ajoutBordure()     
##        self.f.creerCanvas(self.L,self.l, self.tab)
##
##        self.placeMur()
##
##        self.placeSorties()
##        self.placeRobots()
##       
##        
##        
##    def rouletteDown(self,event=None):
##        #rreduit d'une case la matrice
##        print("miaou2")
##                
##    def roulette(self,event):
##        print("test")
##        
##        if event.delta > 0:
##            self.rouletteUp()
##        else:
##            self.rouletteDown()


    def editeur(self):
        
        if askyesno("Attention !","effacer la grille actuel ?") or self.tab== [] :            

            taille = askinteger('Taille Matrice', 'entrez la taille de la nouvelle matrice:',initialvalue=10,minvalue=2)

            #tableau de robots
            self.tabR=[]
            #la matrice
            self.tab= []
            #tableau des sorties
            self.tabS = []
            #tableau des différentes couleur utilisé
            self.tabCouleur = []

            self.bot = 0
            self.exit =0

            self.L = taille
            self.l = taille
            self.tab = [[case() for x in range(self.l)] for y in range(self.L)]
            

            self.f.canvas.destroy() 
            self.ajoutBordure()     
            self.f.creerCanvas(self.L,self.l, self.tab)
            
            self.placeMur()
        
        self.f.canvas.focus_set()

        #self.f.canvas.bind("<B1-Motion>", self.changeCase)

        self.couleurPipette = "red"
    
##
##        if "Linux" in platform.uname()[0]:
##            ##pour comptabilité linux (mollette souris):
##            self.f.canvas.bind("<Button-4>", self.rouletteUp)
##            self.f.canvas.bind("<Button-5>", self.changeCase)
##        else:
##            self.f.canvas.bind("<MouseWheel>", self.roulette)

        self.f.canvas.bind("<Button-1>", self.changeCase)
        self.f.canvas.bind("<Button-3>", self.cliqueDroit)
            

###fin editeur



###pour initialiser matrice via fichier

    #on cree la matri par rapport au fichier fournis
    def creerViaFichier(self):
        self.L = int(self.fichier[0][0])
        self.l = int(self.fichier[0][1])
        self.bot = len(self.fichier[2])//3
        self.exit = len(self.fichier[3])//3

        self.tab = [[case() for x in range(self.l)] for y in range(self.L)]
        
        ##remplis le tableau en indiquant la position des murs
        for i in range((self.L*self.l)):

            #self.tab[x].append(case())


            if "g" in self.fichier[1][i]:
                self.tab[(i)%self.L][(i)//self.L].setGauche(True)
            if "d" in self.fichier[1][i]:
                self.tab[(i)%self.L][(i)//self.L].setDroite(True)
            if "h" in self.fichier[1][i]:
                self.tab[(i)%self.L][(i)//self.L].setHaut(True)
            if "b" in self.fichier[1][i]:
                self.tab[(i)%self.L][(i)//self.L].setBas(True)
              


        ##comme la couleur dans le fichier est un nombre,
            ##nous genererons une couleur aléatoire a partir de se nombre et le stoquerons dans un dico
            ##(pour pouvoir acceder a la couleur grace a se nombre)
        dicoCouleur= {}
            
        ##on place les robots:
        for i in range(0,self.bot*3,3):
            if not (self.fichier[2][i+2] in dicoCouleur ): #si la couleur n'est pas enregistrer 
                dicoCouleur[self.fichier[2][i+2]] =self.genererCouleur() 
                self.tabCouleur.append(dicoCouleur[self.fichier[2][i+2]])
            couleur = dicoCouleur[self.fichier[2][i+2]]
           

            
            self.tabR.append(robot(int(self.fichier[2][i]),int(self.fichier[2][i+1]),couleur))
            self.tab[int(self.fichier[2][i])][int(self.fichier[2][i+1])].setRobot(True)
                       
        ##on place les sortie
        for i in range(0,self.exit*3,3):
            if not (self.fichier[2][i+2] in dicoCouleur ): #si la couleur n'est pas enregistrer 
                dicoCouleur[self.fichier[2][i+2]] =self.genererCouleur() 
            
            couleur = dicoCouleur[self.fichier[2][i+2]]
           
            self.tabS.append(sortie(int(self.fichier[3][i]),int(self.fichier[3][i+1]),couleur))
            self.tab[int(self.fichier[3][i])][int(self.fichier[3][i+1])].setSortie(True)



        self.creerInterface()
                







    #cree la matrice par rapport au paramètre.
    
        
    def creerTab(self):
        for i in range((self.L) ):
            self.tab.append([])
            
            for j in range(self.l):
                
                ##on place des mur aléatoire par rapport a la densite
                self.tab[i].append(case(alea=True, densite= self.densite))

            
                ##on ajoute un mur aux bordures de la grille
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


        if not self.solvable:
            self.initBot()
            self.initSortie()
            self.creerInterface()

        else:
            self.initSolvable()
            self.creerInterface()
            self.melangeRobot(self.mouvement)
            
        #self.creerInterface()
            

        
            


    ##place les robots sur la grille
    def initBot(self):
        a=0
        couleur = "red"
        couleurDiffRestante = self.getCouleurR()
        while a < self.getRobot():
        
            x=randint(0,self.L-1)
            y=randint(0,self.l-1)
            ##si la case est libre, on place le robot
            ##et la case prend le statue "occuper"

            #pour le nombre de couleur differente a utiliser


            if(self.tab[x][y].getRobot()==False):
                if couleurDiffRestante > 0:
                    
                    couleur =self.genererCouleur()
                    ##on stoque la couleur dans un tableau pour avoir des sortie de meme couleur
                    self.tabCouleur.append(couleur)
                    couleurDiffRestante=couleurDiffRestante-1
                else:
                    couleur = random.sample(self.tabCouleur, 1)
                    couleur=couleur[0]
                self.tabR.append(robot(x, y ,couleur))
                self.tab[x][y].setRobot(True)

                a=a+1

    ##place les sortie sur la grille
    def initSortie(self):
        a=0
        couleurDiffRestante = self.getCouleurE()
       
        #copieTab: permet la certitude de tirer une couleur differente
        copieTab = []
        copieTab.extend(self.tabCouleur)

        #si couleur < nbe robot besoin de l'occurance pour des couleur des robots
        #pour correspondre aux mieux aux couleurs des sorties
        tabOccC = []
        for i in range(self.getRobot()):
            tabOccC.append(self.tabR[i].getCouleur())


        
        while a < self.getSortie():
        
            x=randint(0,self.L-1)
            y=randint(0,self.l-1)
            ##place les sortie sur les case libre (ni robot ni sortie)

 
            if(self.tab[x][y].getRobot()==False and self.tab[x][y].getSortie()==False):

                couleur ="red"
                if couleurDiffRestante > 0 and not copieTab == []:
                  
                    
                    
                    couleur = random.sample(copieTab, 1)
                    couleur=couleur[0]

                    tabOccC.remove(couleur)
                    copieTab.remove(couleur)
                    ##on stocke la couleur dans un tableau pour avoir des sortie de meme couleur

                    couleurDiffRestante=couleurDiffRestante-1
                    
                else:

                    if tabOccC == []:
                        couleurUtilise = set(self.tabCouleur)
                        couleur = random.sample(self.tabCouleur,1)                        

                    
                    elif copieTab==[]:
                        couleurUtilise = set(tabOccC)
                        couleur = random.sample(couleurUtilise,1)
                        tabOccC.remove(couleur[0])
                    else:
                        couleurUtilise = set(tabOccC) - set(copieTab)

                        couleur = random.sample(couleurUtilise,1)
                        tabOccC.remove(couleur[0])


                    
                        
                    couleur=couleur[0]


                self.tabS.append(sortie( x, y ,couleur))
                self.tab[x][y].setSortie(True)

                a=a+1



    def initSolvable(self):
        #pour les grille solvable, on suppose qu'il y a autant de robot que de sortie
        #et les occurance de couleur sont identique pour les robot et les sortie.
        #on actualise donc les information pour que cela concorde
        self.exit =  0 
        self.colorE = self.colorR

        self.tabPositionInitiale= []

                           
        a=0
        couleur = "red"
        #pour le nombre de couleur differente a utiliser
        couleurDiffRestante = self.getCouleurR()
        while a < self.getRobot():
        
            x=randint(0,self.L-1)
            y=randint(0,self.l-1)

            ##condition requise:            
            ##-si la case est libre, on place le robot
            ##    et la case prend le statue "occuper"
            ##- on s'assure qu'au moins un mouvement est possible

            if(self.tab[x][y].getRobot()==False and ( self.movePossibleH(x,y) or
                                                      self.movePossibleB(x,y) or
                                                      self.movePossibleG(x,y) or
                                                      self.movePossibleD(x,y) )):
                if couleurDiffRestante > 0:
                    
                    couleur = self.genererCouleur()
                    couleurDiffRestante=couleurDiffRestante-1
                    self.tabCouleur.append(couleur)
                else:
                    couleur = random.sample(self.tabCouleur, 1)
                    couleur=couleur[0]

                
                self.tabR.append(robot(x, y ,couleur))
                self.tab[x][y].setRobot(True)
                self.tabPositionInitiale.append(robot(x, y ,couleur))

                #self.tabS.append(sortie( x, y ,couleur))
                #self.tab[x][y].setSortie(True)

                a=a+1

    def melangeRobot(self, n):

        global lastItem

        aucuneSolution= False

        compteur=0

        tabDernierMove = ["first"]*len(self.tabR)
        
        
        while compteur < n and not aucuneSolution:
            

            tabRobotMove=self.MoveParRobot(tabDernierMove)
            #print(tabRobotMove)
            if tabRobotMove == []:
                aucuneSolution = True
            else:
                
                direction = random.sample(tabRobotMove,1)

                #random.sample renvois une liste, nous avons donc une liste de liste ici
                #un supprime donc la liste inutile
                direction= direction[0]

                ##on enlève l'identifiant pour ne pas le tirer au sort ensuite
                
                #print(direction)

                

                lastItem[0] = self.tabR[direction[0]].getId()
                
                numeroR= direction[0]


                del direction[0]



                trajectoire = random.sample(direction, 1)

                if trajectoire[0] == "haut":
                    self.deplaceH()
                    tabDernierMove[numeroR] = "haut"

                if trajectoire[0] == "bas":
                    self.deplaceB()
                    tabDernierMove[numeroR] = "bas"

                if trajectoire[0] == "gauche":
                    self.deplaceG()
                    tabDernierMove[numeroR] = "gauche"


                if trajectoire[0] == "droite":
                    self.deplaceD()
                    tabDernierMove[numeroR] = "droite"
            
            

            
            compteur=compteur+1
            #print("\n", tabDernierMove,"\n")


        if aucuneSolution:
            print("grille non resolvable pour les n coup demander, \n changemant de grille")
            #on réinitialise les tableau
            self.tabR=[]       
            self.tab= []
            self.tabS = []
            self.tabCouleur = []

            self.creerTab()
        else:
            self.finaliseSolvable()
        
    #########

    def MoveParRobot(self,tabDernierMove):
        tabRobotMove=[]
        
        for i in range(len(self.tabR)):
            x= self.tabR[i].getX()
            y= self.tabR[i].getY()

            compteur=0

            directionAccessible= []
            
            directionAccessible.append( i )


            ##condition requise:
            # -direction non obstrué
            # -le denier mouvement n'est pas la direction contraire(pour ne par retourner
            #     sur ses pas
            # - la direction contraire doit etre un mur (pour qu'on puisse faire le
            #     le chemin dans l'autre sens.

            
            if (self.movePossibleH(x,y)>0 and tabDernierMove[i] != "bas"):
                #and self.movePossibleB(x,y) ==0 ):
                
                compteur=compteur+1
                directionAccessible.append("haut")
                
                    
            if (self.movePossibleB(x,y)>0 and tabDernierMove[i] != "haut"):
                #and self.movePossibleH(x,y) ==0 ):

                compteur=compteur+1
                directionAccessible.append("bas")
                
            if (self.movePossibleG(x,y)>0 and tabDernierMove[i] != "droite"):
                #and self.movePossibleD(x,y) ==0 ):

                compteur=compteur+1
                directionAccessible.append("gauche")

            if (self.movePossibleD(x,y)>0 and tabDernierMove[i] != "gauche"):
                #and self.movePossibleG(x,y) ==0 ):

                compteur=compteur+1
                directionAccessible.append("droite")



            if compteur != 0:

                tabRobotMove.append(directionAccessible)
                


                
        return tabRobotMove
    


                       
                       

    def finaliseSolvable(self):
        
        self.exit =  self.bot

        #on place les sorties avant de modifier les robots pour qu'elles
        #apparaissent au 2ieme plan
        for i in range (self.exit):
            x= self.tabR[i].getX()
            y= self.tabR[i].getY()

            self.tabS.append(sortie( x, y ,self.tabR[i].getCouleur()))

            self.tab[x][y].setSortie(True)

            self.tab[x][y].setRobot(False)
            
            #on place la sortie    
            Id=self.f.placeSortie(self.tabS[i])
            self.tabS[i].setId(Id)

        
        
        for i in range(len(self.tabR)):
            #print(len(self.tabPositionInitiale))
            y=self.tabPositionInitiale[i].getY()
            x=self.tabPositionInitiale[i].getX()
            self.tabR[i].setY(y)
            self.tabR[i].setX(x)
            self.tab[x][y].setRobot( True )
                    
            ##modif de l'interface graphique:
            #print("x = ", x ," et y = ", y)
            self.f.canvas.coords(self.tabR[i].getId(),x*self.f.tailleCase+(self.f.tailleCase/10),y*self.f.tailleCase+(self.f.tailleCase/10),
                                 x*self.f.tailleCase+(self.f.tailleCase/10*9),y*self.f.tailleCase+(self.f.tailleCase/10*9))

            #on place le robot au premier plan pour éviter d'etre "cache" par la sortie
            self.f.canvas.tag_raise(self.tabR[i].getId())            
  




        del self.tabPositionInitiale

        global move
        move=0
        self.f.afficheMove(move)
                
                




    def placeMur(self):
        #on place les murs
        for i in range((self.L) ):
            for j in range(self.l):
                self.f.placeMur(self.tab[i][j],i,j)       

    def placeSorties(self):
        #on place les sorties
        for i in range(self.getSortie()):
            Id=self.f.placeSortie(self.tabS[i])
            self.tabS[i].setId(Id)

    def placeRobots(self):               
        #on place les robots
        for i in range(self.getRobot()):            
            Id = self.f.placeRobot(self.tabR[i])
            ##on lie l'Id du cercle au robot
            self.tabR[i].setId(Id)


    def executePartie(self):
        self.f.canvas.focus_set()
        self.f.canvas.bind("<Button-1>", self.clique)
        
      
    ## Appelle les fonctions nécessaire à l'affichage graphique par rapport
    ## aux données précédemment inscritent dans la grille.
    def creerInterface(self):

        self.f.creerCanvas(self.L,self.l, self.tab)

        self.placeMur()
        self.placeSorties()
        self.placeRobots()

        self.executePartie()


        #self.f.fenetre.mainloop()
        #global gagner
        #if gagner:
         #   break
                
                
####fin initialisation partie            
            
####debut partie:

 
    ##gère l'evenement "clique souris"
    def clique(self,event):
        #permet de savoir l'action a effectuer (selectionner ou déplacer robot)
        global selection

        #permet de garder en mémoire le dernier robot selectionné
        global lastItem

        ##retranscrit le coordonnée souris en coordonnées du canvas
        x = self.f.canvas.canvasx (event.x)
        y = self.f.canvas.canvasy (event.y)
        print(x,"  ", y)
        
        ##Appelle la fionction qui affiche les zones accessibles
        ## et selectionne le robot (stocker dans lastItem)
        if selection==False:
            lastItem=self.f.canvas.find_closest(x, y,start= "robot")
            print(lastItem)
            print(self.f.canvas.itemcget(lastItem, "tags"))
            if self.f.canvas.itemcget(lastItem, "tags")== "robot current":
                selection=True
                ##ajouter couleur des zones accessibles
                self.afficheMoveCase(True)

        ## Appellle la fonction qui efface les zones accessibles
        ##et déplace le robot selectionné  si la direction est correct
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

               
    ##affiche les zone accessible du robot stocké dans "lastItem"
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
                        self.f.canvas.itemconfigure(self.tab[x][y].getId(),fill="#2e93f9")
                    y =  self.tabR[i].getY()
                    for x in range(xmin, xmax+1):
                        self.f.canvas.itemconfigure(self.tab[x][y].getId(),fill="#2e93f9")
                else:
                    for y in range(ymin, ymax+1):
                        self.f.canvas.itemconfigure(self.tab[x][y].getId(),fill="blue")
                    y =  self.tabR[i].getY()
                    for x in range(xmin, xmax+1):
                        self.f.canvas.itemconfigure(self.tab[x][y].getId(),fill="blue")

                





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
        global move
        for i in range(self.getRobot()):
            if self.tabR[i].getId() == lastItem[0]:


                x =  self.tabR[i].getX()
                y =  self.tabR[i].getY()

                compteur = self.movePossibleH(x,y)
                ##si compteur n'est pas nul, le robot a bouge
                if compteur != 0:
                    ##le compteur est incrémenté
                    move=move+1
                    self.f.afficheMove(move)

                    ##Les informations doivent etre actualise:
                    self.tab[x][y].setRobot( False)
                    y=y-compteur ##actualise y
                    self.tab[x][y].setRobot( True )
                    self.tabR[i].setY(y)
                    ##modif de l'interface graphique:
                    #print("x = ", x ," et y = ", y)
                    self.f.canvas.coords(self.tabR[i].getId(),x*self.f.tailleCase+(self.f.tailleCase/10),y*self.f.tailleCase+(self.f.tailleCase/10),
                                 x*self.f.tailleCase+(self.f.tailleCase/10*9),y*self.f.tailleCase+(self.f.tailleCase/10*9))

                    ##on verifie si une sortie a été atteinte
                    self.verifSortie(i,x,y)     

    def deplaceB(self):        
        global lastItem
        global move
        for i in range(self.getRobot()):
            if self.tabR[i].getId() == lastItem[0]:

                x =  self.tabR[i].getX()
                y =  self.tabR[i].getY()
                compteur = self.movePossibleB(x, y)
                
                ##si compteur n'est pas nul, le robot a bouge
                if compteur != 0:
                    ##le compteur est incrémenté
                    move=move+1
                    self.f.afficheMove(move)                        
                    ##Les informations doivent etre actualise:
                    self.tab[x][y].setRobot( False)
                    y=y+compteur ##actualise y
                    self.tab[x][y].setRobot( True )
                    self.tabR[i].setY(y)
                    ##modif de l'interface graphique:
                    #print("x = ", x ," et y = ", y)
                    self.f.canvas.coords(self.tabR[i].getId(),x*self.f.tailleCase+(self.f.tailleCase/10),y*self.f.tailleCase+(self.f.tailleCase/10),
                                 x*self.f.tailleCase+(self.f.tailleCase/10*9),y*self.f.tailleCase+(self.f.tailleCase/10*9))                

                    ##on verifie si une sortie a été atteinte
                    self.verifSortie(i,x,y)     
        
    def deplaceG(self):        
        global lastItem
        global move
        for i in range(self.getRobot()):
            if self.tabR[i].getId() == lastItem[0]:

                x =  self.tabR[i].getX()
                y =  self.tabR[i].getY()
                compteur=self.movePossibleG(x, y)                    

                ##si compteur n'est pas nul, le robot a bouge
                if compteur != 0:
                    ##le compteur est incrémenté
                    move=move+1
                    self.f.afficheMove(move)

                    ##Les informations doivent etre actualise:
                    self.tab[x][y].setRobot( False)
                    x=x-compteur ##actualise x
                    self.tab[x][y].setRobot( True )
                    self.tabR[i].setX(x)
                    ##modif de l'interface graphique:
                    #print("x = ", x ," et y = ", y)
                    self.f.canvas.coords(self.tabR[i].getId(),x*self.f.tailleCase+(self.f.tailleCase/10),y*self.f.tailleCase+(self.f.tailleCase/10),
                                 x*self.f.tailleCase+(self.f.tailleCase/10*9),y*self.f.tailleCase+(self.f.tailleCase/10*9))               

                    ##on verifie si une sortie a été atteinte
                    self.verifSortie(i,x,y)     
             
    def deplaceD(self):        
        global lastItem
        global move
        for i in range(self.getRobot()):
            if self.tabR[i].getId() == lastItem[0]:

                x =  self.tabR[i].getX()
                y =  self.tabR[i].getY()
                compteur=self.movePossibleD(x, y)
                
               ##si compteur n'est pas nul, le robot a bouge
                if compteur != 0:
                    ##le compteur est incrémenté
                    move=move+1

                    self.f.afficheMove(move)

                    ##Les informations doivent etre actualise:
                    self.tab[x][y].setRobot( False)
                    x=x+compteur ##actualise x
                    self.tab[x][y].setRobot( True )
                    self.tabR[i].setX(x)
                    ##modif de l'interface graphique:
                    #print("x = ", x ," et y = ", y)
                    self.f.canvas.coords(self.tabR[i].getId(),x*self.f.tailleCase+(self.f.tailleCase/10),y*self.f.tailleCase+(self.f.tailleCase/10),
                                 x*self.f.tailleCase+(self.f.tailleCase/10*9),y*self.f.tailleCase+(self.f.tailleCase/10*9))               

                    ##on verifie si une sortie a été atteinte
                    self.verifSortie(i,x,y)           

    def verifSortie(self,i,x,y):
        global gagner
      
                    
        if self.tab[x][y].getSortie():
            print("miaou")

            for j in range(self.getSortie()):
                print("x = ", self.tabS[j].getX() ," et y = ", self.tabS[j].getY())
                    
                if self.tabS[j].getX()==x and self.tabS[j].getY() == y:
                    print("couleur tabR:  ",self.tabR[i].getCouleur(),"couleur tabS: ",self.tabS[j].getCouleur())
                    
                    if self.tabR[i].getCouleur() == self.tabS[j].getCouleur():

                        #self.pause()
                        global move
                        print("     vous avez gagner en ",move," coup     ")
                        self.f.labelGagner(move)
                        gagner = True
                        
                        

    def genererCouleur(self):
        rouge = format(randint(20,255), '02x')
        vert =  format(randint(20,255), '02x')
        bleu =  format(randint(0,150), '02x')
        return '#'+ rouge + vert + bleu


    def pause(self):
        global pause
        if not pause:
            self.f.canvas.unbind("<Button-1>",)
            pause = True
        else:
            self.f.canvas.bind("<Button-1>", self.clique)
            pause = False

            

###fonction d'evenement###        


def reset():
    print("reset")
    
    infoRicochet=[]
    for i in range(len(f.recupInfo)-1):
        if f.recupInfo[i].get() == "":
            infoRicochet.append(2)
        else:   
            infoRicochet.append(int(f.recupInfo[i].get()))
    if f.recupInfo[-3].get() == "" or int(f.recupInfo[-3].get()) <= 0:
        hauteur= 10        
    else:
        hauteur=int(f.recupInfo[-3].get())
        
    if f.recupInfo[-2].get() == "" or int(f.recupInfo[-2].get()) <= 0:
        largeur= 10
    else:      
        largeur=int(f.recupInfo[-2].get())
    
    if f.resolve.get()==1:
        ##récup le dernier élémet de la liste
        if f.recupInfo[-1].get() != "":
            tableau=matrice(hauteur,largeur,37,infoRicochet, True,int(f.recupInfo[-1].get()))

        else:
            tableau=matrice(hauteur,largeur,37,infoRicochet, True)
    else:
        tableau=matrice(hauteur,largeur,37,infoRicochet)


    ##l'encienne grille n'est plus référencer et est donc supprimé automatiquement
    #tableau=matrice(10,10,4,infoRicochet)




##fonction pour les zone de selections:
    
def boutonSelection():
    bouton=Button(f.frameSelection, text="Valider", command=reset)
    bouton.grid(column =4,rowspan=3, row=12) #, sticky= "c" )

##fonction pour les zones d'edition

def quitteEditeur():
    global tableau, f
    #on cache la frame de Edition
    f.frameEdition.grid_forget()

    ##et on affiche la frame d'edition
    f.frameSelection.grid(column=4, row=1)
    f.frameSelection.grid_propagate(0)

    f.canvas.unbind("<Button-3>")
    f.canvas.unbind("<Button-4>")
    f.canvas.unbind("<Button-5>")
    f.canvas.unbind("<MouseWheel>")


    #on lance la partie
    tableau.executePartie()

def boutonEdition():
    bouton=Button(f.frameEdition, text="Valider", command=quitteEditeur)
    bouton.grid(column =4,rowspan=3, row=9)





###fonction de sauvegarde et de chargement:   
    
def sauvegarder():
    print("lancement de la sauvegarde...")

    ##pour prevenir une erreur de sauvegarde
    try:
        
        global tableau
        print(tableau)
        if tableau != None:

            
            
            numero=0
            while os.path.isfile("Saves/save("+str(numero)+").ri"):
                numero=numero+1;
            
            nomF="Saves/save("+str(numero)+").ri"


            
            with open(nomF,"w") as fichier:
        
                #print(fichier.read())
                #print("%s,%s;" % (tableau.L, tableau.l))
                
                fichier.write("%s,%s;" % (tableau.L, tableau.l))
                fichier.write("\n\n")
                for j in range(tableau.l):
                    for i in range(tableau.L):
                        donnee=","
                        if tableau.tab[i][j].getHaut():
                            donnee="h"+donnee
                        if tableau.tab[i][j].getBas():
                            donnee="b"+donnee
                        if tableau.tab[i][j].getDroite():
                            donnee="d"+donnee
                        if tableau.tab[i][j].getGauche():
                            donnee="g"+donnee
                        
                        fichier.write(donnee)
                    fichier.write("\n")
                fichier.write("\n;")
                
                ##besoin de créer un nouveau dico de couleur
                    ##car lors de la création nous avons utilisé 2méthode différente
                    ##suivant si on genere la grille a l'aide d'un fichier ou non
                dicoCouleur={}
                for k in range(len(tableau.tabCouleur)):
                    dicoCouleur[tableau.tabCouleur[k]]=k
                
                for r in range(tableau.bot):
                    fichier.write("%s,%s,%s\n," % (tableau.tabR[r].getX(),
                                              tableau.tabR[r].getY() ,
                                              dicoCouleur[tableau.tabR[r].getCouleur()] ))
                fichier.write("\n;")
                for s in range(tableau.exit):                    
                   fichier.write("%s,%s,%s\n," % (tableau.tabS[s].getX(),
                                                 tableau.tabS[s].getY() ,
                                                 dicoCouleur[tableau.tabS[s].getCouleur()] ))
            print("sauvegarde réussi !")
    except:
        print("\n\nerreur survenue lors de la sauvegarde \n(partie non sauvegarde/fichier corrompu)\n\n")

        

##ouvre le fichier, le split et l'envoie a la classe tableau
def chargerFichier(file):
    #pour evitez certaines erreurs:
    with open(file,"r") as fichier:   

        contenu=fichier.read()
        ##on sépare les information (entête, info matrice, robot, sortie)
        contenu = contenu.split(";")
        ##puis on sépare chaque éléments
        for i in range(len(contenu)):
            contenu[i] = contenu[i].split(",")
        tableau=matrice(fichier = contenu)



                   
##initialise le mode édition
def edition():
    global f
    global tableau
    #on cache la frame de Selection
    f.frameSelection.grid_forget()

    ##et on affiche la frame d'edition
    f.frameEdition.grid(column=4, row=1)
    f.frameEdition.grid_propagate(0)

    if tableau == None:
        tableau=matrice(edition=True)
    else:
        tableau.editeur()
    
    



##ouvre la fenetre de dialogue pour charger une partie
def menuCharger():
    filename = askopenfilename(title="Charger la sauvegarde",filetypes=[('Ri files', '*.ri'),('txt files','.txt'),('all files','.*')])    
    chargerFichier(filename)







#import tkinter.colorchooser
#couleur= tkinter.colorchooser.askcolor()

######




#la fenetre du programme
f=interface(Tk())

#f.afficheSaisie()
##savoir si un robot est déjà selectionné
selection= False

##permet de connaitre le dernier robot selectionné
lastItem =[0]

##compteur de mouvement
move=0

##booleen, pour savoir si une sortie a été attteinte par le bon robot
gagner=False

##pour mettre en pause le jeu:
pause=False

#######
#a certainement faire une fonction:
##fais apparaitre la zone de selection a droite
f.zoneSelection()
##pour eviter bug, bouton de validation séparé
boutonSelection()
##
##on crée la zone d'edition
f.zoneEdition()
##et on la cache
f.frameEdition.grid_forget()
boutonEdition()


####

#nbRobot, nbCouleurRobot, nbSortie, nbcouleurSortie
infoRicochet=[2,2,2,2]

##si in fichier est passer en paramètre
##organisation du fichier: [longueur,largeur,hb, gd, etc... 

tableau= None
if len(sys.argv) == 2:
    chargerFichier(sys.argv[1])
        

#par défault
else:      
    tableau=matrice(20,20,40,infoRicochet, solvable = True)
    #reset()




### le menu ###
menubar = Menu(f.fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Commencer", command=reset)
#if tableau !=None:
 #   menu1.add_command(label="pause", command=tableau.pause)
menu1.add_command(label="Sauvegarder", command=sauvegarder)
menu1.add_command(label="Charger", command=menuCharger)
menu1.add_separator()
menu1.add_command(label="Mode Edition", command=edition)
menubar.add_cascade(label="Fichier", menu=menu1)
f.fenetre.config(menu=menubar)










#tableau.f.canvas.focus_set()

#tableau.f.canvas.bind("<Button-1>", tableau.clique)

f.fenetre.mainloop()


