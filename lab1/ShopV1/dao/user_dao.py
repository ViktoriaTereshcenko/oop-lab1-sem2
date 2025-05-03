from database import get_connection

class UserDAO:
    @staticmethod
    def get_user_by_credentials(username, password):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, username, role FROM users
                    WHERE username = %s AND password = %s
                """, (username, password))
                result = cur.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "username": result[1],
                        "role": result[2]
                    }
                return None

    @staticmethod
    def get_user_by_id(user_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, username, role FROM users
                    WHERE id = %s
                """, (user_id,))
                result = cur.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "username": result[1],
                        "role": result[2]
                    }
                return None

    @staticmethod
    def get_all_users():
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, username, role FROM users
                """)
                return [
                    {"id": row[0], "username": row[1], "role": row[2]}
                    for row in cur.fetchall()
                ]

    @staticmethod
    def create_user(username, password, role="user"):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (username, password, role)
                    VALUES (%s, %s, %s)
                """, (username, password, role))
            conn.commit()
