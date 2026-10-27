
from tkinter import messagebox
from db import connect_db


def add_patient(name, age, gender, phone, address, symptoms, visit_date):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        INSERT INTO patients
        (name, age, gender, phone, address, symptoms, visit_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            name, age, gender, phone,
            address, symptoms, visit_date
        )

        cursor.execute(query, values)
        conn.commit()

        messagebox.showinfo("Success", "Patient added successfully!")
        return True

    except Exception as e:
        if conn:
            conn.rollback()

        messagebox.showerror(
            "Error", f"Failed to add patient.\n\nDetails: {e}"
        )
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def search_patient(keyword):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        SELECT * FROM patients
        WHERE name LIKE %s OR phone LIKE %s
        """

        value = f"%{keyword}%"
        cursor.execute(query, (value, value))
        return cursor.fetchall()

    except Exception as e:
        messagebox.showerror(
            "Error", f"Failed to search patients.\n\nDetails: {e}"
        )
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_patient(patient_id, name, age, gender, phone, address, symptoms, visit_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE patients
        SET name=%s, age=%s, gender=%s, phone=%s,
            address=%s, symptoms=%s, visit_date=%s
        WHERE patient_id=%s
        """,
        (name, age, gender, phone, address, symptoms, visit_date, patient_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return True

def delete_patient(patient_id):
    confirm = messagebox.askyesno(
        "Confirm Deletion",
        f"Are you sure you want to delete patient ID {patient_id}?\n\n"
        "This action cannot be undone."
    )

    if not confirm:
        return False

    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM patients WHERE patient_id = %s",
            (patient_id,)
        )

        if cursor.rowcount == 0:
            conn.rollback()
            messagebox.showwarning(
                "Not Found",
                "No patient was deleted. The patient record may not exist."
            )
            return False

        conn.commit()
        messagebox.showinfo("Success", "Patient deleted successfully!")
        return True

    except Exception as e:
        if conn:
            conn.rollback()

        messagebox.showerror(
            "Error", f"Failed to delete patient.\n\nDetails: {e}"
        )
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


    
