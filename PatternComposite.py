import abc


class Employee(abc.ABC):

    def getName(self):
        pass

class Ouvrier(Employee):

    def __init__(self,name):
        self.name = name

    def getName(self):
        return self.name

class Manager(Employee):

    def __init__(self,name):
        self.ListE = []
        self.name = name

    def getName(self):
        return self.name

    def giveall(self):
        print(self.getName())
        for employee in self.ListE:
            if "ListE" in employee.__dict__ :
                employee.giveall()


            else :
                print(employee.getName())



ouvrier = Ouvrier("herve")
manager = Manager("topmanager")
manager1 = Manager("manager")
manager1.ListE.append(ouvrier)

manager.ListE.append(manager1)


manager.giveall()



