# test_db.py
import mysql.connector, sys
try:
    conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', port=3306, database='task_manager')
    print("CONNECTED OK")
    conn.close()
except Exception as e:
    print("ERROR:", type(e).__name__, e)
    sys.exit(1)
