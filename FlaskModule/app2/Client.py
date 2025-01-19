import requests

# Base URL of your Flask API
BASE_URL = "http://localhost:5002"  # Change this if your Flask app is running on a different host or port


# Function to get all products
def get_all_products():
    response = requests.get(f"{BASE_URL}/products")
    if response.status_code == 200:
        print("Products retrieved successfully:")
        products = response.json()
        for product in products:
            print(product)
    else:
        print("Failed to retrieve products:", response.status_code, response.text)


# Function to get a random product
def get_random_product():
    response = requests.get(f"{BASE_URL}/product")
    if response.status_code == 200:
        print("Random Product retrieved successfully:")
        product = response.json()
        print(product)
    else:
        print("Failed to retrieve product:", response.status_code, response.text)


# Testing the functions
if __name__ == "__main__":
    print("Getting all products:")
    get_all_products()

    print("\nGetting random product:")
    get_random_product()
