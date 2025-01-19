
from flask import Blueprint, jsonify, request

from controle import Control

main = Blueprint("main", __name__)

Control.createProduct()

Control.fill_product("baname","vert","cameroun","de boe saveur")
Control.fill_product("avocat","vert","cameroun","le bon avocat")
@main.route("/")
def index():
    return jsonify({"message": "Welcome to the Flask PostgreSQL API!"})


# Récupérer tous les produits
@main.route("/products", methods=["GET"])
def get_products():
    products = Control.getAllProduct()
    return products


# Récupérer un produit  aleatoire
@main.route("/product", methods=["GET"])
def get_product():
    product = Control.findProduct()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return product


