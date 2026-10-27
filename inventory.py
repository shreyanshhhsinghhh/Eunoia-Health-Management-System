from tkinter import messagebox
from db import connect_db


def add_item(item_name, category, quantity, price, supplier):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        INSERT INTO inventory
        (item_name, category, quantity, price, supplier)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (item_name, category, quantity, price, supplier)

        cursor.execute(query, values)
        item_id = cursor.lastrowid
        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Inventory item added successfully!\nItem ID: {item_id}"
        )
        return True

    except Exception as e:
        if conn:
            conn.rollback()

        messagebox.showerror(
            "Error",
            f"Failed to add inventory item.\n\nDetails: {e}"
        )
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_item(item_id, item_name, category, quantity, price, supplier):
    conn = None
    cursor = None

    try:
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

        if cursor.rowcount == 0:
            conn.rollback()
            messagebox.showwarning(
                "No Changes",
                "No inventory item was updated. The item may not exist, "
                "or the details may be unchanged."
            )
            return False

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Inventory item ID {item_id} updated successfully!"
        )
        return True

    except Exception as e:
        if conn:
            conn.rollback()

        messagebox.showerror(
            "Error",
            f"Failed to update inventory item.\n\nDetails: {e}"
        )
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_item(item_id):
    confirm = messagebox.askyesno(
        "Confirm Deletion",
        f"Are you sure you want to delete inventory item ID {item_id}?\n\n"
        "This action cannot be undone."
    )

    if not confirm:
        return False

    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = "DELETE FROM inventory WHERE item_id = %s"
        cursor.execute(query, (item_id,))

        if cursor.rowcount == 0:
            conn.rollback()
            messagebox.showwarning(
                "Not Found",
                f"No inventory item found with ID {item_id}."
            )
            return False

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Inventory item ID {item_id} deleted successfully!"
        )
        return True

    except Exception as e:
        if conn:
            conn.rollback()

        messagebox.showerror(
            "Error",
            f"Failed to delete inventory item.\n\nDetails: {e}"
        )
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_all_items():
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = "SELECT * FROM inventory ORDER BY item_name"
        cursor.execute(query)
        data = cursor.fetchall()

        return data

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Failed to retrieve inventory.\n\nDetails: {e}"
        )
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_low_stock_items():
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        SELECT * FROM inventory
        WHERE quantity < 5
        ORDER BY quantity ASC
        """
        cursor.execute(query)
        data = cursor.fetchall()

        return data

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Failed to retrieve low-stock items.\n\nDetails: {e}"
        )
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

