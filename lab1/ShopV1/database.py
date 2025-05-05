import psycopg

def get_connection():
    return psycopg.connect(
        host="localhost",
        dbname="shop",
        user="vikilinater",
        password="admin"
    )
