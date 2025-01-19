from numpy.ma.core import append


class Logfile(object):

    @staticmethod
    def instance():
        if "_instance" not in Logfile.__dict__:

            Logfile._instance = Logfile()
            Logfile.write_to_file(message=Logfile.__name__)
        Logfile.write_to_file(message=Logfile.__name__)

        return Logfile._instance

    def write_to_file(self,logfile="log.txt",message=""):
        filew = open(logfile, "w+", encoding="utf8")
        filew.write(message)
        filew.close()

    def readfile(self):
        read = open("log.txt","rt",encoding="utf8")
        print(read.readlines())
        read.close()



lg1 = Logfile.instance()
lg1.readfile()

