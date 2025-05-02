from db import get_connection

class ProductDAO:
    @staticmethod
    def get_all_products():
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, description, price FROM products")
                return [
                    {"id": row[0], "name": row[1], "description": row[2], "price": row[3]}
                    for row in cur.fetchall()
                ]

    @staticmethod
    def get_product(product_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, description, price FROM products WHERE id = %s", (product_id,))
                row = cur.fetchone()
                if row:
                    return {"id": row[0], "name": row[1], "description": row[2], "price": row[3]}
                return None

    @staticmethod
    def add_product(name, description, price):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO products (name, description, price)
                    VALUES (%s, %s, %s)
                """, (name, description, price))
            conn.commit()

    @staticmethod
    def update_product(product_id, name, description, price):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE products
                    SET name = %s, description = %s, price = %s
                    WHERE id = %s
                """, (name, description, price, product_id))
            conn.commit()

    @staticmethod
    def delete_product(product_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
