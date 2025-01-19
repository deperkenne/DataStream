import random


class Products:
    __List_product = []

    def getAllProducts(self):
        return self.__List_product

    def findProduct(self):
        product = random.choice(self.__List_product)
        return product

    def addProduct(self,name,color,origin,description):
        dictio = {}
        dictio.__setitem__("name", name)
        dictio.__setitem__("color", color)
        dictio.__setitem__("origin", origin)
        dictio.__setitem__("description", description)

        Products.__List_product.append(dictio)
