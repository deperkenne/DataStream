import abc
from abc import abstractmethod

class Street:
    def __init__(self,ville,rue):
          self.ville = ville
          self.rue = rue

class VendorToAdapt:
    _name:str
    _age:str
    _street:Street

    def getName(self,name):
        self._name = name
        return self._name
    def getAge(self,age):
        self._age = age
        return self._age
    def getStreet(self,street):
        self._street = street
        return self._street.ville + self._street.rue
class AbsAdaptor(abc.ABC):
    @abstractmethod
    def getName(self, name):
        pass
    @abstractmethod
    def getStreet(self,street):
        pass
    @property
    def getAge(self,age):
        pass

class Adoptorvendor1(AbsAdaptor):
    def __init__(self):
        self._vendor = VendorToAdapt()
    def getName(self,name):
        return self._vendor.getName(name)
    def getStreet(self,street):
        return self._vendor.getStreet(street)

class Adoptorvendor2(AbsAdaptor):
    def __init__(self):
        self._vendor = VendorToAdapt()
    def getAge(self,age):
        return self._vendor.getAge(age)





adoptorvendor = Adoptorvendor()
print(adoptorvendor.getStreet(Street("kribi","dombe")))
print(adoptorvendor.getName("kenne"))




class Absclass(abc.ABC):
    def __init__(self,vendortoAdapt:VendorToAdapt):
              self._vendor = vendortoAdapt
    @property
    def getVendor(self):
        return self._vendor

    @abc.abstractproperty
    def getName(self):
        pass

    @abc.abstractproperty
    def getStreetiunfo(self):
        pass


class AdaptatorVendor(Absclass):
    @property
    def getName(self):
        return self.vendor.name
    @property
    def getStreetiunfo(self):
        return self.vendor.ville + self.vendor.rue


