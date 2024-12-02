def get_uoms(connection):
    """
    Fetches all Unit of Measurement (UOM) records from the database.

    Args:
        connection: Active MySQL database connection.

    Returns:
        A list of dictionaries where each dictionary represents a UOM with its ID and name.
    """
    cursor = connection.cursor()

    # Query to fetch all UOMs
    uoms_query = ("SELECT uom_id, uom_name FROM uom")
    cursor.execute(uoms_query)

    # Process the results into a list of dictionaries
    response = [
        {
            'uom_id': uom_id,
            'uom_name': uom_name
        }
        for (uom_id, uom_name) in cursor
    ]
    cursor.close()  # Close the cursor after use

    return response


if __name__ == '__main__':
    from sql_connection import get_sql_connection

    # Establish a connection to the database
    connection = get_sql_connection()

    # Fetch and print all UOMs
    print(get_uoms(connection))
