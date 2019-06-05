try:
    import Tkinter as Tk
except:
    import tkinter as Tk
 


 
def OnValidate(S,P):
    if S.isdigit():
        print(S)
        print(P)
        if P == "" or int(P,10) <= 100:
            return True
    return False
 
root = Tk.Tk()
validatecmd = (root.register(OnValidate), '%S', '%P')
e = Tk.Entry(root, validate="key", vcmd=validatecmd,width=6)
e.pack()


valeur= Tk.IntVar()
spamCB  = Tk.Checkbutton(root, text='Spam?',
    variable=valeur, onvalue=1, offvalue=0)



print(valeur.get())
#spamVar = StringVar()
#spamCB  = Tk.Checkbutton(root, text='Spam?',variable=spamVar, onvalue=True, offvalue=False)
#spamCB.pack()
#spamVar.set('oui')
print(spamCB)

root.mainloop()
