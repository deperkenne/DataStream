from flask import Flask, jsonify
import psycopg2
import requests

app = Flask(__name__)


# Configuration de la connexion à PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='your_db_name',
        user='your_db_user',
        password='your_db_password'
    )
    return conn


# Fonction pour récupérer des données depuis l'API (Amazon ou autre)
def fetch_data_from_api():
    url = "https://api.example.com/products"  # Remplacez par l'URL de l'API
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []


# Route pour récupérer les produits stockés dans la base de données
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products;')
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(products)


# Route pour ajouter des produits à la base de données à partir de l'API
@app.route('/update_products', methods=['GET'])
def update_products():
    products_data = fetch_data_from_api()

    if products_data:
        conn = get_db_connection()
        cursor = conn.cursor()

        for product in products_data:
            name = product.get('name')
            price = product.get('price')
            description = product.get('description')

            cursor.execute('''
                INSERT INTO products (name, price, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (name) DO NOTHING;
            ''', (name, price, description))

        conn.commit()
        cursor.close()
        conn.close()

        return "Products updated successfully", 200
    else:
        return "No data found", 400


if __name__ == '__main__':
    app.run(debug=True)