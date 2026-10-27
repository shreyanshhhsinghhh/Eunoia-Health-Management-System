
from db import connect_db


def get_dashboard_data():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bills")
    total_bills = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total) FROM bills")
    total_revenue = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT COUNT(*) FROM bills WHERE payment_status = 'Pending'"
    )
    pending_payments = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total_patients, total_bills, total_revenue, pending_payments

