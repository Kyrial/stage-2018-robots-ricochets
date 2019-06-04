from tkinter import *
import random


#####CLASS INTERFACE#####

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
                
        
        self.canvas.grid(column =0, row=1, columnspan=2,rowspan = 9)
        self.creerLabelNbMove()

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
        self.canvas.tag_raise(identifiant)

        return identifiant

    def placeSortie(self,sortie):
       
        identifiant = self.canvas.create_rectangle((sortie.getX()*50)+5,(sortie.getY()*50)+5,
                                (sortie.getX()*50)+45,(sortie.getY()*50)+45,
                                fill=sortie.getCouleur(), tags="Sortie")

        return identifiant



    def creerLabelNbMove(self):
        self.phrase = Label(self.fenetre, text="Nombres de déplacements: ",font=20)
        self.phrase.grid(column =0, row=0, sticky= "e" )
        self.score = Label(self.fenetre, text="0",font=20)
        self.score.grid(column =1, row=0, sticky= "w" )

    def labelGagner(self, compteur):
        self.score.configure(text= str(compteur) + " mouvement, Bravo !    ")
        self.phrase.configure(text= "           Vous avez gagné en ")



    def afficheMove(self, compteur):
        self.score.configure(text=compteur)


    def zoneSelection(self):

        self.creerLabel(1,"Entrez le nombres de Robots")
        self.creerLabel(3,"Entrez le nombres de \n couleurs de Robots")
        self.creerLabel(5,"Entrez le nombres de sorties")
        self.creerLabel(7,"Entrez le nombres de \n couleurs de Robots")

        self.recupInfo = []
        for i in range(2,9,2):
            self.recupInfo.append( self.afficheSaisie(i))

    #    bouton=Button(self.fenetre, text="Valider", command=self.resetBouton)
     #   bouton.grid(column =3, row=9) #, sticky= "c" )

        

    def creerLabel(self,position, texte):
        Label(self.fenetre, text = texte, font=20).grid(column =3, row=position, sticky= "s" )
 

    def afficheSaisie(self,i):        
        validatecmd = (self.fenetre.register(OnValidate), '%S', '%P')
        e = Entry(self.fenetre, validate="key", vcmd=validatecmd,width=6)
        e.grid(column =3, row=i, sticky= "n" )
        return e

##
##    def resetBouton(self):
##        print("reset")
##        if self.recupInfo[0].get() == "":
##            print("miaouuuuu")
##
##        ##l'encienne grille n'est plus référencer et est donc supprimé automatiquement
##        from Matrice import reset
##
##        reset()
##        

    
        
    






def OnValidate(S,P):
    if S.isdigit():

        if P == "" or int(P,10) <= 100:
            return True
    return False








