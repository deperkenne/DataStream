import abc
import copy
from abc import abstractmethod


class AbsColor(abc.ABC):
    @abstractmethod
    def getRedColor(self):
     pass
    @abstractmethod
    def getBlauColor(self):
        pass

class Color(AbsColor):
    def __init__(self,color:str):
        self.color = color
    def getRedColor(self):
        return self.color
    def getBlauColor(self):
        pass

class Forme(abc.ABC):
    @abstractmethod
    def getColor(self,color:Color):
        pass
    @abstractmethod
    def getName(self,name):
        pass

class Carre(Forme):

    def getColor(self, color: Color):
         return color.getRedColor()

    def getName(self, name):
        return name

carre = Carre()

print(carre.getColor(Color("red")) + carre.getName("carrerouge"))
carre2 = copy.deepcopy(carre)
print(carre.getColor(Color("blue")) + carre.getName("blue"))

