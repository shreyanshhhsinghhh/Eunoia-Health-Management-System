from db import connect_db

def add_appointment(patient_id, patient_name, doctor_name, appointment_date, appointment_time, status):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO appointments
    (patient_id, patient_name, doctor_name, appointment_date, appointment_time, status)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (patient_id, patient_name, doctor_name, appointment_date, appointment_time, status)

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


def get_all_appointments():
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT * FROM appointments ORDER BY appointment_date, appointment_time"
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

def update_appointment(appointment_id, patient_id, patient_name, doctor_name, appointment_date, appointment_time, status):
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

    values = (patient_id, patient_name, doctor_name, appointment_date, appointment_time, status, appointment_id)

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


def delete_appointment(appointment_id):
    conn = connect_db()
    cursor = conn.cursor()

    query = "DELETE FROM appointments WHERE appointment_id = %s"
    cursor.execute(query, (appointment_id,))

    conn.commit()
    cursor.close()
    conn.close()
