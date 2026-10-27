
from tkinter import messagebox
from db import connect_db


def add_doctor(doctor_name, specialization, phone, email, availability):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        INSERT INTO doctors
        (doctor_name, specialization, phone, email, availability)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (doctor_name, specialization, phone, email, availability)

        cursor.execute(query, values)
        doctor_id = cursor.lastrowid
        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Doctor added successfully!\nDoctor ID: {doctor_id}"
        )
        return True

    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Error", f"Failed to add doctor.\n\nDetails: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_doctor(
    doctor_id, doctor_name, specialization, phone, email, availability
):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        UPDATE doctors
        SET doctor_name = %s,
            specialization = %s,
            phone = %s,
            email = %s,
            availability = %s
        WHERE doctor_id = %s
        """
        values = (
            doctor_name, specialization, phone, email,
            availability, doctor_id
        )

        cursor.execute(query, values)

        if cursor.rowcount == 0:
            conn.rollback()
            messagebox.showwarning(
                "Notice",
                "No changes made, or doctor not found."
            )
            return False

        conn.commit()
        messagebox.showinfo("Success", "Doctor updated successfully!")
        return True

    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror(
            "Error", f"Failed to update doctor.\n\nDetails: {e}"
        )
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_doctor(doctor_id):
    if not messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete doctor ID {doctor_id}?"
    ):
        return False

    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = "DELETE FROM doctors WHERE doctor_id = %s"
        cursor.execute(query, (doctor_id,))

        if cursor.rowcount == 0:
            conn.rollback()
            messagebox.showwarning("Notice", "Doctor not found.")
            return False

        conn.commit()
        messagebox.showinfo("Success", "Doctor deleted successfully!")
        return True

    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror(
            "Error", f"Failed to delete doctor.\n\nDetails: {e}"
        )
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_all_doctors():
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        SELECT *
        FROM doctors
        ORDER BY doctor_name
        """
        cursor.execute(query)
        return cursor.fetchall()

    except Exception as e:
        messagebox.showerror(
            "Error", f"Failed to load doctors.\n\nDetails: {e}"
        )
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
