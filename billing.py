from tkinter import messagebox
from db import connect_db


def add_bill(patient_id, consultation_fee, medicine_cost, payment_status, bill_date):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        total = consultation_fee + medicine_cost

        query = """
        INSERT INTO bills
        (patient_id, consultation_fee, medicine_cost, total,
         payment_status, bill_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            patient_id,
            consultation_fee,
            medicine_cost,
            total,
            payment_status,
            bill_date
        )

        cursor.execute(query, values)
        bill_id = cursor.lastrowid
        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Bill created successfully!\nBill ID: {bill_id}\n"
            f"Total Amount: ₹{total:.2f}"
        )
        return True

    except Exception as e:
        if conn:
            conn.rollback()

        messagebox.showerror(
            "Error",
            f"Failed to create bill.\n\nDetails: {e}"
        )
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_bill_by_id(bill_id):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = "SELECT * FROM bills WHERE bill_id = %s"
        cursor.execute(query, (bill_id,))
        bill = cursor.fetchone()

        if bill is None:
            messagebox.showwarning(
                "Not Found",
                f"No bill found with ID {bill_id}."
            )

        return bill

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Failed to retrieve bill.\n\nDetails: {e}"
        )
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_bill(bill_id):
    confirm = messagebox.askyesno(
        "Confirm Deletion",
        f"Are you sure you want to delete bill ID {bill_id}?\n\n"
        "This action cannot be undone."
    )

    if not confirm:
        return False

    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = "DELETE FROM bills WHERE bill_id = %s"
        cursor.execute(query, (bill_id,))

        if cursor.rowcount == 0:
            conn.rollback()
            messagebox.showwarning(
                "Not Found",
                f"No bill found with ID {bill_id}. Nothing was deleted."
            )
            return False

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Bill ID {bill_id} deleted successfully!"
        )
        return True

    except Exception as e:
        if conn:
            conn.rollback()

        messagebox.showerror(
            "Error",
            f"Failed to delete bill.\n\nDetails: {e}"
        )
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_bill(bill_id, consultation_fee, medicine_cost, payment_status, bill_date):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        total = consultation_fee + medicine_cost

        query = """
        UPDATE bills
        SET consultation_fee = %s,
            medicine_cost = %s,
            total = %s,
            payment_status = %s,
            bill_date = %s
        WHERE bill_id = %s
        """

        values = (
            consultation_fee,
            medicine_cost,
            total,
            payment_status,
            bill_date,
            bill_id
        )

        cursor.execute(query, values)

        if cursor.rowcount == 0:
            conn.rollback()
            messagebox.showwarning(
                "No Changes",
                "No bill was updated. The bill may not exist, "
                "or the details may be unchanged."
            )
            return False

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Bill ID {bill_id} updated successfully!\n"
            f"Updated Total: ₹{total:.2f}"
        )
        return True

    except Exception as e:
        if conn:
            conn.rollback()

        messagebox.showerror(
            "Error",
            f"Failed to update bill.\n\nDetails: {e}"
        )
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


    

