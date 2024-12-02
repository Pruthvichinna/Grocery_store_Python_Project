from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    """
    Inserts a new order into the database, including the order details.

    Args:
        connection: Active MySQL database connection.
        order: A dictionary containing order information:
            - customer_name: Name of the customer.
            - grand_total: Total amount for the order.
            - order_details: List of products in the order, each with:
                - product_id: ID of the product.
                - quantity: Quantity ordered.
                - total_price: Total price for the product.

    Returns:
        The ID of the newly inserted order.
    """
    cursor = connection.cursor()

    # Query to insert the main order into the 'orders' table
    order_query = (" INSERT INTO orders (customer_name, total, datetime) VALUES (%s, %s, %s)")
    order_data = (order['customer_name'], order['grand_total'], datetime.now())
    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid  # Get the ID of the newly created order

    # Query to insert order details into the 'order_details' table
    order_details_query = ("INSERT INTO order_details (order_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)")
    order_details_data = [
        (
            order_id,
            int(detail['product_id']),
            float(detail['quantity']),
            float(detail['total_price'])
        )
        for detail in order['order_details']
    ]
    cursor.executemany(order_details_query, order_details_data)  # Insert multiple rows at once
    connection.commit()

    return order_id

def get_order_details(connection, order_id):
    """
    Fetches the details of a specific order.

    Args:
        connection: Active MySQL database connection.
        order_id: ID of the order to fetch details for.

    Returns:
        A list of dictionaries where each dictionary represents a product in the order.
    """
    cursor = connection.cursor()

    # Query to fetch order details by order ID
    order_details_query = ("SELECT order_details.order_id, order_details.quantity, order_details.total_price, products.name, products.price_per_unit FROM order_details LEFT JOIN products ON order_details.product_id = products.product_id WHERE order_details.order_id = %s")
    cursor.execute(order_details_query, (order_id,))

    records = [
        {
            'order_id': order_id,
            'quantity': quantity,
            'total_price': total_price,
            'product_name': product_name,
            'price_per_unit': price_per_unit
        }
        for (order_id, quantity, total_price, product_name, price_per_unit) in cursor
    ]
    cursor.close()

    return records

def get_all_orders(connection):
    """
    Fetches all orders from the database, including their details.

    Args:
        connection: Active MySQL database connection.

    Returns:
        A list of dictionaries where each dictionary represents an order with its details.
    """
    cursor = connection.cursor()

    # Query to fetch all orders
    orders_query = ("SELECT order_id, customer_name, total, datetime FROM orders")
    cursor.execute(orders_query)

    # Process the query results into dictionaries
    response = [
        {
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': dt
        }
        for (order_id, customer_name, total, dt) in cursor
    ]
    cursor.close()

    # Append order details to each order
    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])

    return response

if __name__ == '__main__':
    # Establish a connection to the database
    connection = get_sql_connection()

    # Example usage of the functions
    print(get_all_orders(connection))
    # Uncomment below lines to test other functions:
    # print(get_order_details(connection, 4))
    # print(insert_order(connection, {
    #     'customer_name': 'John Doe',
    #     'grand_total': 500,
    #     'order_details': [
    #         {'product_id': 1, 'quantity': 2, 'total_price': 50},
    #         {'product_id': 3, 'quantity': 1, 'total_price': 30}
    #     ]
    # }))
