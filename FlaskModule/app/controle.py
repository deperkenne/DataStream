
from modele2 import Products


class Control:
    products:Products
    @staticmethod
    def createProduct():
        Control.products = Products()
    @staticmethod
    def fill_product(name,color,origin,description):
        Control.products.addProduct(name,color,origin,description)
    @staticmethod
    def getAllProduct():
        return Control.products.getAllProducts()
    @staticmethod
    def findProduct():
        return Control.products.findProduct()

