import os
import psycopg

def get_connection():
    return psycopg.connect(
        host="localhost",
        dbname=os.environ.get("DB_NAME", "your_db_name"),
        user=os.environ.get("DB_USER", "your_db_user"),
        password=os.environ.get("DB_PASSWORD", "your_db_password")
    )
