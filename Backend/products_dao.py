from sql_connection import get_sql_connection

def get_all_products(connection):
    """
    Fetches all products from the database along with their details.
    
    Args:
        connection: Active MySQL database connection.

    Returns:
        A list of dictionaries where each dictionary represents a product with its details.
    """
    cursor = connection.cursor()

    # SQL query to join 'products' and 'uom' tables to fetch product details
    query = (" SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name FROM products INNER JOIN uom ON products.uom_id = uom.uom_id")
    cursor.execute(query)

    # Initialize an empty list to hold the product details
    response = []
    # Iterate through the query results and format them into dictionaries
    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'uom_id': uom_id,
            'price_per_unit': price_per_unit,
            'uom_name': uom_name
        })

    return response

def insert_new_product(connection, product):
    """
    Inserts a new product into the database.

    Args:
        connection: Active MySQL database connection.
        product: A dictionary containing the product details (name, uom_id, price_per_unit).

    Returns:
        The ID of the newly inserted product.
    """
    cursor = connection.cursor()

    # SQL query to insert a new product
    query = (" INSERT INTO products (name, uom_id, price_per_unit) VALUES (%s, %s, %s)")
    # Data tuple for the query
    data = (product['product_name'], product['uom_id'], product['price_per_unit'])

    # Execute the query with the data
    cursor.execute(query, data)
    connection.commit()  # Commit the transaction to save changes

    return cursor.lastrowid  # Return the ID of the newly inserted product

def delete_product(connection, product_id):
    """
    Deletes a product from the database based on the product ID.

    Args:
        connection: Active MySQL database connection.
        product_id: The ID of the product to be deleted.

    Returns:
        The ID of the deleted product.
    """
    cursor = connection.cursor()

    # SQL query to delete a product by its ID
    query = f"DELETE FROM products WHERE product_id = {product_id}"

    # Execute the query
    cursor.execute(query)
    connection.commit()  # Commit the transaction to save changes

    return product_id  # Return the ID of the deleted product

if __name__ == '__main__':
    # Establish a database connection
    connection = get_sql_connection()

    # Uncomment the following lines to test each function:

    # Test fetching all products
    # print(get_all_products(connection))

    # Test deleting a product
    # print(delete_product(connection, 12))

    # Test inserting a new product
    print(insert_new_product(connection, {
        'product_name': 'potatoes',
        'uom_id': '1',
        'price_per_unit': 10
    }))
