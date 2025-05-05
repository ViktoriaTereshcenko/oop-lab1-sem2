from dao.user_dao import UserDAO

def add_initial_users():
    users = [
        ("admin", "admin", "admin"),
        ("user", "user123", "user"),
    ]
    for i in range(1, 6):
        users.append((f"user_{i}", f"pass_{i}", "user"))

    dao = UserDAO()
    for username, password, role in users:
        try:
            dao.create_user(username, password, role)
            print(f"User created: {username}")
        except Exception as e:
            print(f"Skipped user {username}: {e}")

if __name__ == "__main__":
    add_initial_users()
