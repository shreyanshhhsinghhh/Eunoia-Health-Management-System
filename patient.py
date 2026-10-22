from db import connect_db

def add_patient(name, age, gender, phone, address, symptoms, visit_date):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    insert into patients (name, age, gender, phone, address, symptoms, visit_date)
    values (%s,%s,%s,%s,%s,%s,%s)
    """

    values = (name,age,gender,phone,address,symptoms,visit_date)

    cursor.execute(query,values)
    conn.commit()
    cursor.close()
    conn.close()

def search_patient(keyword):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT * FROM patients
    WHERE name LIKE %s OR phone LIKE %s
    """

    value = f"%{keyword}%"
    cursor.execute(query, (value, value))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def update_patient(patient_id, name, age, gender, phone, address, symptoms,):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    UPDATE patients
    SET name = %s,
            age = %s,
            gender = %s,
            phone = %s,
            address = %s,
            symptoms = %s
    WHERE patient_id = %s
    """

    values = (name, age, gender, phone, address, symptoms, patient_id)

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

def delete_patient(patient_id):
    conn = connect_db()
    cursor = conn.cursor()

    query = "DELETE FROM patients WHERE patient_id =%s"
    cursor.execute(query, (patient_id,))

    conn.commit()
    cursor.close()
    conn.close()
    
    
