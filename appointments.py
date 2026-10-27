from tkinter import messagebox
from db import connect_db


def add_appointment(
    patient_id, patient_name, doctor_name,
    appointment_date, appointment_time, status
):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        INSERT INTO appointments
        (patient_id, patient_name, doctor_name,
         appointment_date, appointment_time, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            patient_id, patient_name, doctor_name,
            appointment_date, appointment_time, status
        )

        cursor.execute(query, values)
        appointment_id = cursor.lastrowid
        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Appointment booked successfully!\n"
            f"Appointment ID: {appointment_id}"
        )
        return True

    except Exception as e:
        if conn:
            conn.rollback()

        messagebox.showerror(
            "Error",
            f"Failed to book appointment.\n\nDetails: {e}"
        )
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_all_appointments():
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        SELECT * FROM appointments
        ORDER BY appointment_date, appointment_time
        """
        cursor.execute(query)
        data = cursor.fetchall()

        return data

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Failed to retrieve appointments.\n\nDetails: {e}"
        )
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_appointment(
    appointment_id, patient_id, patient_name, doctor_name,
    appointment_date, appointment_time, status
):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        UPDATE appointments
        SET patient_id = %s,
            patient_name = %s,
            doctor_name = %s,
            appointment_date = %s,
            appointment_time = %s,
            status = %s
        WHERE appointment_id = %s
        """

        values = (
            patient_id, patient_name, doctor_name,
            appointment_date, appointment_time, status,
            appointment_id
        )

        cursor.execute(query, values)

        if cursor.rowcount == 0:
            conn.rollback()
            messagebox.showwarning(
                "No Changes",
                "No appointment was updated. It may not exist, "
                "or the details may be unchanged."
            )
            return False

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Appointment ID {appointment_id} updated successfully!"
        )
        return True

    except Exception as e:
        if conn:
            conn.rollback()

        messagebox.showerror(
            "Error",
            f"Failed to update appointment.\n\nDetails: {e}"
        )
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_appointment(appointment_id):
    confirm = messagebox.askyesno(
        "Confirm Deletion",
        f"Are you sure you want to delete appointment ID "
        f"{appointment_id}?\n\nThis action cannot be undone."
    )

    if not confirm:
        return False

    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = "DELETE FROM appointments WHERE appointment_id = %s"
        cursor.execute(query, (appointment_id,))

        if cursor.rowcount == 0:
            conn.rollback()
            messagebox.showwarning(
                "Not Found",
                f"No appointment found with ID {appointment_id}."
            )
            return False

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Appointment ID {appointment_id} deleted successfully!"
        )
        return True

    except Exception as e:
        if conn:
            conn.rollback()

        messagebox.showerror(
            "Error",
            f"Failed to delete appointment.\n\nDetails: {e}"
        )
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

