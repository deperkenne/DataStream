import abc

from click import command


class Command(abc.ABC):
    def  execute(self):
        pass

class Interface(abc.ABC):
    def eteindre(self):
        pass
    def allume(self):
        pass
    def augmenteV(self):
        pass
    def diminuV(self):
        pass

class Television(Interface):
    def eteindre(self):
        print("tele eteind")

    def allume(self):
        print("tele allumer")

class Radio(Interface):
    def eteindre(self):
        print("radio etteind")

    def allume(self):
        print("radio allumer")

class Allumer(Command):
      def __init__(self,interface):
          self.interface = interface

      def execute(self):
          self.interface.allume(self)

class Etteindre(Command) :
    def __init__(self,interface):
        self.interface=interface
    def execute(self):
        self.interface.eteindre(self)

class Remote:
    def __init__(self):
        self.command = None

    def setCommande(self,command):
       self.command = command



remote = Remote()
remote.setCommande(Allumer(Radio))
remote.command.execute()
remote.setCommande(Etteindre(Radio))
remote.command.execute()
remote.setCommande(Allumer(Television))
remote.command.execute()
