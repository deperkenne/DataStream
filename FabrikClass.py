from DessignPatter import *


class FabrikCar:

    def factory_methode(self,name:str,model_list:list[str]):
            list_car = [CarInterface]
            if name == "Benz":
                 for model in model_list:
                     if model in ["sport","lixus"] and model == "sport":
                          list_car.append(Benz(name,model))
                     if model in ["sport","lixus"] and model == "lixus":
                         list_car.append(Benz(name,model))
            elif name == "Audit":
                for model in model_list:
                    if model in ["sport", "lixus"] and model == "sport":
                        list_car.append(Audit(name,model))
                    if model in ["sport", "lixus"] and model == "lixus":
                        list_car.append(Audit(name,model))
            return list_car



