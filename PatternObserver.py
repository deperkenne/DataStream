import abc


class Abo(abc.ABC):
    def affiche(self,message):
        pass

class Entreprise(Abo):
    def affiche(self,message):
        print(Entreprise.__name__,message)
class Eleve(Abo):
    def affiche(self,message):
        print(Eleve.__name__,message)


class Fourniseur:
    listAbo = []

    def addAbo(self,abo:Abo):
        self.listAbo.append(abo)

    def sendinfo(self,message):
        for abo in self.listAbo:
            abo.affiche(message)

fournisseur = Fourniseur()
fournisseur.addAbo(Eleve())
fournisseur.addAbo(Entreprise())
fournisseur.sendinfo("desormais le credit coute 500")