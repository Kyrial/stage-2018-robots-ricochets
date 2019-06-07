from tkinter import *
#try:
#    import Tkinter as Tk
#except:
#    import tkinter as Tk
 
class interface:

    def __init__(self, fen ):
        self.fenetre = fen


    def creerCanvas(self, L, l, case=0):
        self.canvas = Canvas(self.fenetre, width=600, height=600,
                             borderwidth=5,background="white")
        self.canvas['scrollregion'] = (-25,-25,575,575)

        self.tailleCase= max(L,l)        
    
        for li in range(0,L):
            for co in range(0,l):
               # Id= self.canvas.create_rectangle(50*li,50*co,50*li+50,50*co+50,
                #                        fill='blue', tags= 'carre')
                Id= self.canvas.create_rectangle(li*(550/self.tailleCase),co*(550/self.tailleCase),
                                                 (li+1)*(550/self.tailleCase),(co+1)*(550/self.tailleCase),
                                        fill='blue', tags= 'carre')


                
        
        self.canvas.grid(column =0, row=1, columnspan=2,rowspan = 11)
        self.creerLabelNbMove()



 
def OnValidate(S,P):
    if S.isdigit():
        print(S)
        print(P)
        if P == "" or int(P,10) <= 100:
            return True
    return False

f=interface(Tk())
f.creerCanvas(10,10)


##
##root = Tk()
##validatecmd = (root.register(OnValidate), '%S', '%P')
##e = Tk.Entry(root, validate="key", vcmd=validatecmd,width=6)
##e.pack()
##
##
##valeur= IntVar()
##spamCB  = Checkbutton(root, text='Spam?',
##    variable=valeur, onvalue=1, offvalue=0)
##


#print(valeur.get())
#spamVar = StringVar()
#spamCB  = Tk.Checkbutton(root, text='Spam?',variable=spamVar, onvalue=True, offvalue=False)
#spamCB.pack()
#spamVar.set('oui')
#print(spamCB)

f.fenetre.mainloop()
