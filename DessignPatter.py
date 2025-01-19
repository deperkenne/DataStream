from abc import ABC

class CarInterface(ABC):
     def getModel(self):
         pass
     def getName(self):
         pass

class Benz(CarInterface):
    def __init__(self,name,model_name):
        self.__model = model_name
        self.__name = name

    def getModel(self):
        return self.__model
    def getName(self):
        return self.__name

class Audi(CarInterface):
    def __init__(self, name, model_name):
        self.__model = model_name
        self.__name = name

    def getModel(self):
        return self.__model

    def getName(self):
        return self.__name
