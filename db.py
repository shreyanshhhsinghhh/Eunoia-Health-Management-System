


import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="---",
        database="hospital_db"
    )
    return conn

if __name__ == "__main__":
    try:
        conn = connect_db()
        print("connected successfully")
        conn.close()
    except Exception as e:
        print("Error:", e)
