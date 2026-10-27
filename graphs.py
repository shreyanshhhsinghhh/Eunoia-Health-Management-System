import matplotlib.pyplot as plt
from db import connect_db


def show_revenue_graph():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DATE(bill_date), SUM(total)
        FROM bills
        WHERE bill_date >= CURDATE() - INTERVAL 4 DAY
          AND bill_date < CURDATE() + INTERVAL 1 DAY
        GROUP BY DATE(bill_date)
        ORDER BY DATE(bill_date) ASC
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    dates = [str(row[0]) for row in data]
    revenue = [float(row[1] or 0) for row in data]

    plt.figure()
    plt.plot(dates, revenue, marker='o')
    plt.title("Revenue Per Day (Last 5 Days)")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def show_patient_graph():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DATE(visit_date), COUNT(*)
        FROM patients
        WHERE visit_date >= CURDATE() - INTERVAL 4 DAY
          AND visit_date < CURDATE() + INTERVAL 1 DAY
        GROUP BY DATE(visit_date)
        ORDER BY DATE(visit_date) ASC
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    dates = [str(row[0]) for row in data]
    counts = [row[1] for row in data]

    plt.figure()
    plt.bar(dates, counts)
    plt.title("Patients Per Day (Last 5 Days)")
    plt.xlabel("Date")
    plt.ylabel("Number of Patients")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def show_payment_pie():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT payment_status, COUNT(*)
        FROM bills
        GROUP BY payment_status
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    labels = [row[0] or "Unknown" for row in data]
    values = [float(row[1] or 0) for row in data]

    plt.figure(figsize=(6, 6))

    print("Payment chart values:", values)
    print("Payment chart total:", sum(values))

    if not values or sum(values) <= 0:
        plt.text(
            0.5, 0.5,
            "No payment data yet",
            ha="center",
            va="center",
            transform=plt.gca().transAxes
        )
        plt.title("Payment Status")
        plt.axis("off")

    else:
        plt.pie(
            values,
            labels=None,
            autopct='%1.1f%%',
            pctdistance=0.78,
            startangle=90,
            wedgeprops=dict(width=0.4),
            explode=[0.02] * len(values)
        )
        plt.title("Payment Status", y=1.08)
        plt.axis("equal")
        plt.legend(
            labels,
            loc="upper center",
            bbox_to_anchor=(0.5, 1.02),
            ncol=3
        )

    plt.tight_layout()
    plt.show()


def show_gender_graph():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT gender, COUNT(*)
        FROM patients
        GROUP BY gender
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    genders = [row[0] or "Unknown" for row in data]
    counts = [row[1] for row in data]

    plt.figure(figsize=(6, 5))
    plt.bar(genders, counts)
    plt.title("Gender Distribution")
    plt.xlabel("Gender")
    plt.ylabel("Number of Patients")
    plt.tight_layout()
    plt.show()
