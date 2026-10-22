from db import connect_db

def add_item(item_name, category, quantity, price, supplier):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO inventory (item_name, category, quantity, price, supplier)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (item_name, category, quantity, price, supplier)

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


def update_item(item_id, item_name, category, quantity, price, supplier):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    UPDATE inventory
    SET item_name = %s,
        category = %s,
        quantity = %s,
        price = %s,
        supplier = %s
    WHERE item_id = %s
    """
    values = (item_name, category, quantity, price, supplier, item_id)

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


def delete_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()

    query = "DELETE FROM inventory WHERE item_id = %s"
    cursor.execute(query, (item_id,))

    conn.commit()
    cursor.close()
    conn.close()


def get_all_items():
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT * FROM inventory ORDER BY item_name"
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

def get_low_stock_items():
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT * FROM inventory WHERE quantity < 10 ORDER BY quantity ASC"
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data
