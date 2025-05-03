from database import get_connection

class BlacklistDAO:
    @staticmethod
    def add_to_blacklist(user_id, reason):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO blacklist (user_id, reason)
                    VALUES (%s, %s)
                """, (user_id, reason))
            conn.commit()

    @staticmethod
    def is_user_blacklisted(user_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM blacklist WHERE user_id = %s", (user_id,))
                return cur.fetchone() is not None

    @staticmethod
    def get_blacklist():
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT users.username, blacklist.reason, blacklist.created_at
                    FROM blacklist
                    JOIN users ON users.id = blacklist.user_id
                    ORDER BY blacklist.created_at DESC
                """)
                return [
                    {"username": row[0], "reason": row[1], "created_at": row[2]}
                    for row in cur.fetchall()
                ]

    @staticmethod
    def remove_user_from_blacklist(user_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM blacklist WHERE user_id = %s", (user_id,))
            conn.commit()
