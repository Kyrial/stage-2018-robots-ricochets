##fichier graphes
##

from Matrice import *


##
##class graphe:
##
##    def __init__(self, matrice, nbRobot, nbsortie,listeRobot,listeSortie):
##        
##        self.tab=matrice
##        self.nbRobot=nbRobot
##        self.nbSortie=nbSortie
##        self.listeR=listeRobot
##        self.listeS=listeSortie
##
##        
##        
##


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
    try:
    
        with open(file,"r") as fichier:   

            contenu=fichier.read()
            ##on sépare les information (entête, info matrice, robot, sortie)
            contenu = contenu.split(";")
            ##puis on sépare chaque éléments
            for i in range(len(contenu)):
                contenu[i] = contenu[i].split(",")
            tableau=matrice(fichier = contenu)

    except FileNotFoundError:
        print("nom fichier invalide")



                   
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

