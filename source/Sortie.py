#####CLASS SORTIE#####

class sortie:
    def __init__(self, x, y, couleur):
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

