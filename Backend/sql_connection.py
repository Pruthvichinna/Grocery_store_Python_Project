import datetime
import mysql.connector

# Global variable to hold the MySQL connection
__cnx = None

def get_sql_connection():
    """
    Establishes and returns a MySQL database connection.
    
    If a connection does not already exist, this function creates one.
    Subsequent calls will reuse the existing connection.
    
    Returns:
        mysql.connector.connection.MySQLConnection: An active MySQL connection object.
    """
    print("Opening MySQL connection")
    global __cnx

    # Check if the connection is already initialized
    if __cnx is None:
        # Create a new connection to the MySQL database
        __cnx = mysql.connector.connect(
            user='root',          # MySQL username
            password='root',      # MySQL password
            database='grocery_store'  # Name of the database to connect to
        )

    return __cnx
