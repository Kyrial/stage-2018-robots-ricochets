from tkinter import *
import random
from math import *

#####CLASS INTERFACE#####

class interface:

    def __init__(self, fen ):
        self.fenetre = fen
        self.fenetre.title('Jeu Ricochet')


    def creerCanvas(self, L, l, case,LiCaseExclure = []):
        self.canvas = Canvas(self.fenetre,  width=600, height=600,
                             borderwidth=5,background="white")
        self.canvas['scrollregion'] = (-25,-25,575,575)

        self.tailleCase= (550/max(L,l))

        for li in range(0,L):
            for co in range(0,l):
                #print( "li :",li , "co : ", co)
                
                if case[li][co] == 0 or (li,co) in LiCaseExclure:
                    self.canvas.create_rectangle(li*self.tailleCase,co*self.tailleCase,
                                                 (li+1)*self.tailleCase,(co+1)*self.tailleCase,
                                        fill='#2c2c2c',outline='#2c2c2c', tags= 'exterieur')
                    if (li,co) in LiCaseExclure:
                        case[li][co].setExterieur(True)
                else:                    
                    Id= self.canvas.create_rectangle(li*self.tailleCase,co*self.tailleCase,
                                                 (li+1)*self.tailleCase,(co+1)*self.tailleCase,
                                        fill='blue', tags= 'carre')
                    case[li][co].setId(Id)
                    ##on pourrait placer les mur directement ici
                    #self.PlaceMur(
                
        
        self.canvas.grid(column =2, row=1, columnspan=2) #,rowspan = 11)
        self.creerLabelNbMove()

    def placeMur(self, cases, x, y):
    
        if cases.getHaut():
            self.canvas.create_line(x*self.tailleCase   , y*self.tailleCase   , (x+1)*self.tailleCase , y*self.tailleCase,
                                    width=6-log(5*self.tailleCase,10),tags= str(cases.getId())+"h")
        if cases.getBas():
            self.canvas.create_line(x*self.tailleCase   , (y+1)*self.tailleCase, (x+1)*self.tailleCase , (y+1)*self.tailleCase,
                                    width=6-log(5*self.tailleCase,10),tags= str(cases.getId())+"b")
        if cases.getDroite():
            self.canvas.create_line((x+1)*self.tailleCase, y*self.tailleCase   , (x+1)*self.tailleCase , (y+1)*self.tailleCase,
                                    width=6-log(5*self.tailleCase,10),tags= str(cases.getId())+"d")
        if cases.getGauche():
            self.canvas.create_line(x*self.tailleCase   , y*self.tailleCase   , x*self.tailleCase    , (y+1)*self.tailleCase,
                                    width=6-log(5*self.tailleCase,10),tags= str(cases.getId())+"g")
    def placeRobot(self,robot):
       
        identifiant = self.canvas.create_oval(robot.getX()*self.tailleCase+(self.tailleCase/10),(robot.getY()*self.tailleCase)+(self.tailleCase/10),
                                (robot.getX()*self.tailleCase)+(self.tailleCase/10*9),(robot.getY()*self.tailleCase)+(self.tailleCase/10*9),
                                fill=robot.getCouleur(), tags="robot")
        self.canvas.tag_raise(identifiant)

        return identifiant

    def placeSortie(self,sortie):
       
        identifiant = self.canvas.create_rectangle((sortie.getX()*self.tailleCase+(self.tailleCase/10)),(sortie.getY()*self.tailleCase+(self.tailleCase/10)),
                                (sortie.getX()*self.tailleCase+(self.tailleCase/10*9)),(sortie.getY()*self.tailleCase+(self.tailleCase/10*9)),
                                fill=sortie.getCouleur(), tags="Sortie")

        return identifiant


    def traceFleche(self,liste):
       
        liste = list(map(lambda x:( x[0]*self.tailleCase+(self.tailleCase/2)
                                    ,x[1]*self.tailleCase+(self.tailleCase/2)), liste))
        
        self.canvas.create_line(liste,arrow = "first",width = 3)
        



    def creerLabelNbMove(self):
        self.phrase = Label(self.fenetre, text="Nombres de d??placements: ",font=20)
        self.phrase.grid(column =2, row=0, sticky= "e" )
        self.score = Label(self.fenetre, text="0",font=20)
        self.score.grid(column =3, row=0, sticky= "w" )

    def labelGagner(self, compteur):
        ##probleme de dexture si on modifie seulement le Label
        
        
        self.score.configure(text= str(compteur) + " mouvement, Bravo !    ")
        self.phrase.configure(text= "           Vous avez gagn?? en ")



    def afficheMove(self, compteur):
        self.score.configure(text=compteur)


    def zoneSelection(self):
        self.frameSelection = Frame(self.fenetre, borderwidth=2,height =615,width = 250,  relief=GROOVE)
        self.frameSelection.grid(column=4, row=1)
        self.frameSelection.grid_propagate(0)
    

        self.creerLabel(1,"Entrez le nombres de Robots")
        self.creerLabel(3,"Entrez le nombres de \n couleurs de Robots")
        self.creerLabel(5,"Entrez le nombres de sorties")
        self.creerLabel(7,"Entrez le nombres de \n couleurs de Robots")
        self.creerLabel(10,"Entrez respectivement: \n hauteur et largeur",1)
        self.creerLabel(13,"si resolvable, \n en combien de coup",1)
        self.recupInfo = []
        for i in range(2,9,2):
            self.recupInfo.append( self.afficheSaisie(i))

        self.recupInfo.append( self.afficheSaisie(11,colonne=3,colonnespan=1))
        self.recupInfo.append( self.afficheSaisie(11,colonne=4,colonnespan=1))
        
        self.recupInfo.append( self.afficheSaisie(14,colonnespan=1))



        ##variable de controle
        self.resolve= IntVar()
        Checkbutton(self.frameSelection, text="resolvable",variable=self.resolve, onvalue=1, offvalue=0).grid(column =3, row=12,sticky= "s")

        

    def creerLabel(self, ligne, texte,colonnespan = 2):
        Label(self.frameSelection, text = texte, font=20,pady = 10).grid(column =3,columnspan = colonnespan, row=ligne, sticky= "s" )


    def afficheSaisie(self,ligne,colonne=3,colonnespan=2):        
        validatecmd = (self.fenetre.register(OnValidate), '%S', '%P')
        e = Entry(self.frameSelection, validate="key", vcmd=validatecmd,width=6)
        e.grid(column =colonne, row=ligne,columnspan = colonnespan,pady = 10, sticky= "n" )
        return e


    def zoneEdition(self):
        self.frameEdition = Frame(self.fenetre, borderwidth=2,height =615,width = 250,  relief=GROOVE)
        self.frameEdition.grid(column=4, row=1)
        self.frameEdition.grid_propagate(0)
        self.editionCarre()

    def editionCarre(self):

        self.imageHaut = PhotoImage(file="Images/murHaut.png")
        self.imageBas = PhotoImage(file="Images/murBas.png")
        self.imageDroite = PhotoImage(file="Images/murDroite.png")
        self.imageGauche = PhotoImage(file="Images/murGauche.png")
        ##variable de controle
        self.caseCocher= StringVar()
        
        Checkbutton(self.frameEdition,image=self.imageHaut,variable=self.caseCocher,
                    onvalue="haut", offvalue="",pady = 10).grid(column =0, row=1,sticky= "s")

      
        Checkbutton(self.frameEdition,image=self.imageGauche,variable=self.caseCocher,
                    onvalue="gauche", offvalue="",pady = 10).grid(column =0, row=2,sticky= "s")
        
        Checkbutton(self.frameEdition,image=self.imageBas,variable=self.caseCocher,
                    onvalue="bas", offvalue="",pady = 10).grid(column =0, row=3,sticky= "s")        

        Checkbutton(self.frameEdition,image=self.imageDroite,variable=self.caseCocher,
                    onvalue="droite", offvalue="",pady = 10).grid(column =0, row=4,sticky= "s")



        Checkbutton(self.frameEdition,text="robot",variable=self.caseCocher,
                    onvalue="robot", offvalue="",pady = 10).grid(column =0, row=5,sticky= "s")

        Checkbutton(self.frameEdition,text="sortie",variable=self.caseCocher,
                    onvalue="sortie", offvalue="",pady = 10).grid(column =0, row=6,sticky= "s")
##
##
##        self.memeCouleurCocher=StringVar()
##        Checkbutton(self.frameEdition,text="pour les robots/sortie \n garder meme couleur ?",variable=self.memeCouleurCocher,
##                    onvalue="yes", offvalue="",pady = 10).grid(column =1, row=5,rowspan = 2)#,sticky= "s")
##



def OnValidate(S,P):
    if S.isdigit():
        if P == "" or int(P,10) <= 100:
            return True
    return False








