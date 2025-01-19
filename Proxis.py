import abc
from abc import abstractmethod


class BambergMembers(abc.ABC):
    @abstractmethod
    def getMemberName(self):
        pass
class Etudiant(BambergMembers):
    def __init__(self,name):
        self.name = name
    def getMemberName(self):
         return self.name

class Professor(BambergMembers):
    def __init__(self, name):
        self.name = name

    def getMemberName(self):
        return self.name

class DocApi:

    def getListeMembers(self):
        lsitMenmbers = ["etudiant","professeur"]
        return lsitMenmbers
    def getName(self):
        return "etudiant"

class ProxiConrolAccess:
    docApi: DocApi

    def control(self,bambergMembers:BambergMembers):
        if bambergMembers.getMemberName() == "admin":
            ProxiConrolAccess.docApi = DocApi()
            return ProxiConrolAccess.docApi
        elif bambergMembers.getMemberName() != "dev":
            ProxiConrolAccess.docApi = DocApi()
            return ProxiConrolAccess.docApi.getName()
        else:
            print("no authorisation")

proxic = ProxiConrolAccess()
proxi=proxic.control(Professor("admin"))
print(proxi.getListeMembers())






