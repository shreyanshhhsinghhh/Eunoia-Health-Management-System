from db import connect_db

def add_bill(patient_id, consultation_fee, medicine_cost, payment_status, bill_date):
    conn = connect_db()
    cursor = conn.cursor()

    total = consultation_fee + medicine_cost

    query = """
    insert into bills (patient_id , consultation_fee, medicine_cost,total, payment_status, bill_date)
    values (%s, %s, %s, %s, %s, %s)
    """

    values = (patient_id, consultation_fee, medicine_cost, total, payment_status, bill_date)


    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()



def get_bill_by_id(bill_id):
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT * FROM bills WHERE bill_id = %s"
    cursor.execute(query, (bill_id,))
    bill = cursor.fetchone()

    cursor.close()
    conn.close()

    return bill

def delete_bill(bill_id):
    conn = connect_db()
    cursor = conn.cursor()

    query = "DELETE FROM bills WHERE bill_id =%s"
    cursor.execute(query,(bill_id,))

    conn.commit()
    cursor.close()
    conn.close()

def update_bill(bill_id, consultation_fee, medicine_cost, payment_status, bill_date):
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

    values = (consultation_fee, medicine_cost, total, payment_status, bill_date, bill_id)

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    

