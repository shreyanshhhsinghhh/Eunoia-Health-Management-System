from db import connect_db

def add_doctor(doctor_name, specialization, phone, email, availability):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO doctors (doctor_name, specialization, phone, email, availability)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (doctor_name, specialization, phone, email, availability)

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


def update_doctor(doctor_id, doctor_name, specialization, phone, email, availability):
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
    values = (doctor_name, specialization, phone, email, availability, doctor_id)

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


def delete_doctor(doctor_id):
    conn = connect_db()
    cursor = conn.cursor()

    query = "DELETE FROM doctors WHERE doctor_id = %s"
    cursor.execute(query, (doctor_id,))

    conn.commit()
    cursor.close()
    conn.close()


def get_all_doctors():
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT * FROM doctors ORDER BY doctor_name"
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data
