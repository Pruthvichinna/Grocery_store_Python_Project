from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
import mysql.connector
import json

# DAO modules for handling database operations
import products_dao
import orders_dao
import uom_dao

# Initialize Flask application
app = Flask(__name__)

# Establish database connection
connection = get_sql_connection()

# Endpoint to fetch all units of measurement (UOMs)
@app.route('/getUOM', methods=['GET'])
def get_uom():
    """
    Fetches all units of measurement (UOM) from the database.
    
    Returns:
        JSON response containing the list of UOMs.
    """
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Enable CORS
    return response

# Endpoint to fetch all products
@app.route('/getProducts', methods=['GET'])
def get_products():
    """
    Fetches all products from the database.
    
    Returns:
        JSON response containing the list of products.
    """
    response = products_dao.get_all_products(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Enable CORS
    return response

# Endpoint to insert a new product
@app.route('/insertProduct', methods=['POST'])
def insert_product():
    """
    Inserts a new product into the database.
    
    Expects:
        JSON payload with product details in the 'data' field.
    
    Returns:
        JSON response with the ID of the inserted product.
    """
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')  # Enable CORS
    return response

# Endpoint to fetch all orders
@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    """
    Fetches all orders from the database.
    
    Returns:
        JSON response containing the list of orders.
    """
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Enable CORS
    return response

# Endpoint to insert a new order
@app.route('/insertOrder', methods=['POST'])
def insert_order():
    """
    Inserts a new order into the database.
    
    Expects:
        JSON payload with order details in the 'data' field.
    
    Returns:
        JSON response with the ID of the inserted order.
    """
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')  # Enable CORS
    return response

# Endpoint to delete a product
@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    """
    Deletes a product from the database based on its ID.
    
    Expects:
        Form data with 'product_id'.
    
    Returns:
        JSON response with the ID of the deleted product.
    """
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')  # Enable CORS
    return response

# Entry point for the Flask application
if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(port=5000)
