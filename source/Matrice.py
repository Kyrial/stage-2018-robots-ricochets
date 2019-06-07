from tkinter import *
import random


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
    def __init__(self, longueur, largeur, densite, infoRicochet, solvable = False,mouvement=10):
        self.reinitialise()
        self.L = longueur
        self.l = largeur

        self.densite = densite
        self.solvable= solvable
        self.mouvement=mouvement
        
        self.bot = infoRicochet[0]
        self.tabR=[]
        
        self.colorR = infoRicochet[1]
        self.exit = infoRicochet[2]
        self.colorE = infoRicochet[3]
        self.tab= []
        self.tabS = []
        self.tabCouleur = []

        
        self.creerTab()

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
        print(self.getCouleurE())
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
            print(tabRobotMove)
            if tabRobotMove == []:
                aucuneSolution = True
            else:
                
                direction = random.sample(tabRobotMove,1)

                #random.sample renvois une liste, nous avons donc une liste de liste ici
                #un supprime donc la liste inutile
                direction= direction[0]

                ##on enlève l'identifiant pour ne pas le tirer au sort ensuite
                
                print(direction)

                

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
            
            print(compteur)

            
            compteur=compteur+1
            print("\n", tabDernierMove,"\n")


        if aucuneSolution:
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
  


        for i in range(len(self.tabR)):
            print(self.tabR[i].getX(), " et ",self.tabR[i].getY() )
            

        del self.tabPositionInitiale

        global move
        move=0
        self.f.afficheMove(move)
                
                



        
      
    ## Appelle les fonctions nécessaire à l'affichage graphique par rapport
    ## aux données précédemment inscritent dans la grille.
    def creerInterface(self):
        global f
        self.f=f
        self.f.creerCanvas(self.L,self.l, self.tab)

        #on place les murs
        for i in range((self.L) ):
            for j in range(self.l):
                self.f.placeMur(self.tab[i][j],i,j)

        #on place les sorties
        for i in range(self.getSortie()):
            Id=self.f.placeSortie(self.tabS[i])
            self.tabS[i].setId(Id)
                
        #on place les robots
        for i in range(self.getRobot()):            
            Id = self.f.placeRobot(self.tabR[i])

            ##on lie l'Id du cercle au robot
            self.tabR[i].setId(Id)


        self.f.canvas.focus_set()

        self.f.canvas.bind("<Button-1>", self.clique)

        #self.f.fenetre.mainloop()
        #global gagner
        #if gagner:
         #   break
                
                
            
            


 
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
                    print("x = ", x ," et y = ", y)
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
                    print("x = ", x ," et y = ", y)
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
                    print("x = ", x ," et y = ", y)
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
                    print("x = ", x ," et y = ", y)
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
    print(f.resolve.get())
    infoRicochet=[]
    for i in range(len(f.recupInfo)-1):
        if f.recupInfo[i].get() == "":
            infoRicochet.append(2)
        else:   
            infoRicochet.append(int(f.recupInfo[i].get()))
    
    
    if f.resolve.get()==1:
        ##récup le dernier élémet de la liste
        if f.recupInfo[-1].get() != "":
            tableau=matrice(10,10,37,infoRicochet, True,int(f.recupInfo[-1].get()))

        else:
            tableau=matrice(10,10,37,infoRicochet, True)
    else:
        tableau=matrice(10,10,37,infoRicochet)


    ##l'encienne grille n'est plus référencer et est donc supprimé automatiquement
    #tableau=matrice(10,10,4,infoRicochet)

    
def bouton():
    bouton=Button(f.fenetre, text="Valider", command=reset)
    bouton.grid(column =4,rowspan=3, row=9) #, sticky= "c" )
    
    

    
    
    





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

##fais apparaitre la zone de selection a droite
f.zoneSelection()
##pour eviter bug, bouton de validation séparé
bouton()



#nbRobot, nbCouleurRobot, nbSortie, nbcouleurSortie
infoRicochet=[2,2,2,2]
                
tableau=matrice(20,20,40,infoRicochet, solvable = True)





### le menu ###
menubar = Menu(f.fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="commencer", command=reset)
menu1.add_command(label="pause", command=tableau.pause)
menubar.add_cascade(label="Fichier", menu=menu1)
f.fenetre.config(menu=menubar)





#tableau.f.canvas.focus_set()

#tableau.f.canvas.bind("<Button-1>", tableau.clique)

f.fenetre.mainloop()

