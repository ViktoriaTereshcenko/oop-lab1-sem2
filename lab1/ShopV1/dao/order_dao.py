from database import get_connection

class OrderDAO:
    @staticmethod
    def get_all_orders():
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT o.id, o.user_id, o.is_paid, o.created_at, u.username
                    FROM orders o
                    JOIN users u ON o.user_id = u.id
                    ORDER BY o.created_at DESC
                """)
                return [
                    {
                        "id": row[0],
                        "user_id": row[1],
                        "status": "paid" if row[2] else "unpaid",
                        "created_at": row[3],
                        "username": row[4]
                    }
                    for row in cur.fetchall()
                ]

    @staticmethod
    def get_orders_by_user(user_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, user_id, is_paid, created_at
                    FROM orders
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                """, (user_id,))
                return [
                    {
                        "id": row[0],
                        "user_id": row[1],
                        "status": "paid" if row[2] else "unpaid",
                        "created_at": row[3]
                    }
                    for row in cur.fetchall()
                ]

    @staticmethod
    def create_order(user_id, product_id, quantity, is_paid=False):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO orders (user_id, product_id, quantity, is_paid)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, user_id, product_id, quantity, is_paid, created_at
                """, (user_id, product_id, quantity, is_paid))
                row = cur.fetchone()
                conn.commit()
                return {
                    "id": row[0],
                    "user_id": row[1],
                    "product_id": row[2],
                    "quantity": row[3],
                    "status": "paid" if row[4] else "unpaid",
                    "created_at": row[5]
                }

    @staticmethod
    def mark_order_paid(order_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE orders
                    SET is_paid = TRUE
                    WHERE id = %s
                """, (order_id,))
                conn.commit()

    @staticmethod
    def update_payment_status(order_id, is_paid):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE orders
                    SET is_paid = %s
                    WHERE id = %s
                """, (is_paid, order_id))
                conn.commit()
