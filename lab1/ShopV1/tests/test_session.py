import unittest
from session import SessionManager, sessions

class TestSessionManager(unittest.TestCase):

    def test_generate_session_id(self):
        session_id = SessionManager.generate_session_id()
        self.assertEqual(len(session_id), 32)

    def test_create_session(self):
        user_id = 123
        session_id = SessionManager.create_session(user_id)
        self.assertIn(session_id, sessions)
        self.assertEqual(sessions[session_id]["user_id"], user_id)
        self.assertEqual(sessions[session_id]["role"], "client")

    def test_get_session_data_valid(self):
        user_id = 123
        session_id = SessionManager.create_session(user_id)
        cookie_header = f"session_id={session_id}"
        session_data = SessionManager.get_session_data(cookie_header)
        self.assertEqual(session_data["user_id"], user_id)

    def test_get_session_data_invalid_cookie(self):
        cookie_header = "session_id=invalid_session_id"
        session_data = SessionManager.get_session_data(cookie_header)
        self.assertIsNone(session_data)

    def test_get_session_user_id(self):
        user_id = 123
        session_id = SessionManager.create_session(user_id)
        cookie_header = f"session_id={session_id}"
        user_id_from_session = SessionManager.get_session_user_id(cookie_header)
        self.assertEqual(user_id_from_session, user_id)

    def test_get_session_user_id_invalid_cookie(self):
        cookie_header = "session_id=invalid_session_id"
        user_id_from_session = SessionManager.get_session_user_id(cookie_header)
        self.assertIsNone(user_id_from_session)

    def test_clear_session_valid(self):
        user_id = 123
        session_id = SessionManager.create_session(user_id)
        cookie_header = f"session_id={session_id}"
        self.assertIn(session_id, sessions)
        SessionManager.clear_session(cookie_header)
        self.assertNotIn(session_id, sessions)

    def test_clear_session_invalid(self):
        cookie_header = "session_id=invalid_session_id"
        SessionManager.clear_session(cookie_header)
        self.assertEqual(len(sessions), 0)

    def test_set_user_role(self):
        user_id = 123
        session_id = SessionManager.create_session(user_id)
        cookie_header = f"session_id={session_id}"
        SessionManager.set_user_role(user_id, "admin")
        self.assertEqual(sessions[session_id]["role"], "admin")

    def test_delete_session(self):
        user_id = 123
        session_id = SessionManager.create_session(user_id)
        self.assertIn(session_id, sessions)
        SessionManager.delete_session(session_id)
        self.assertNotIn(session_id, sessions)

if __name__ == "__main__":
    unittest.main()
