
"""
from flask import Blueprint, jsonify, request
from __init__ import db
from model import Product

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return jsonify({"message": "Welcome to the Flask PostgreSQL API!"})


# Récupérer tous les produits
@main.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])


# Récupérer un produit par ID
@main.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict())


# Créer un nouveau produit
@main.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")
    description = data.get("description")

    if not name or not price:
        return jsonify({"error": "Name and price are required"}), 400

    new_product = Product(name=name, price=price, description=description)
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201


# Mettre à jour un produit
@main.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.description = data.get("description", product.description)

    db.session.commit()
    return jsonify(product.to_dict())


# Supprimer un produit
@main.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})

"""