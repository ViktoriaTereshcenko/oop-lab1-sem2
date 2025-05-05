import unittest
from session import SessionManager

class TestSessionManager(unittest.TestCase):

    def setUp(self):
        SessionManager.sessions.clear()

    def test_create_session(self):
        user_id = 1
        session_id = SessionManager.create_session(user_id)
        self.assertIn(session_id, SessionManager.sessions)
        self.assertEqual(SessionManager.sessions[session_id]['user_id'], user_id)
        self.assertEqual(SessionManager.sessions[session_id]['role'], 'client')

    def test_get_session_data_valid(self):
        user_id = 2
        session_id = SessionManager.create_session(user_id)
        cookie_header = f"session_id={session_id}"
        session_data = SessionManager.get_session_data(cookie_header)
        self.assertIsNotNone(session_data)
        self.assertEqual(session_data['user_id'], user_id)

    def test_get_session_data_invalid(self):
        cookie_header = "session_id=nonexistent"
        self.assertIsNone(SessionManager.get_session_data(cookie_header))

    def test_get_session_user_id(self):
        user_id = 3
        session_id = SessionManager.create_session(user_id)
        cookie_header = f"session_id={session_id}"
        self.assertEqual(SessionManager.get_session_user_id(cookie_header), user_id)

    def test_get_session_user_id_invalid(self):
        self.assertIsNone(SessionManager.get_session_user_id("session_id=invalid"))

    def test_clear_session_valid(self):
        user_id = 4
        session_id = SessionManager.create_session(user_id)
        cookie_header = f"session_id={session_id}"
        SessionManager.clear_session(cookie_header)
        self.assertNotIn(session_id, SessionManager.sessions)

    def test_clear_session_invalid(self):
        SessionManager.clear_session("session_id=wrong")
        self.assertEqual(len(SessionManager.sessions), 0)

    def test_set_user_role(self):
        user_id = 5
        session_id = SessionManager.create_session(user_id)
        SessionManager.set_user_role(user_id, "admin")
        self.assertEqual(SessionManager.sessions[session_id]["role"], "admin")

    def test_delete_session(self):
        user_id = 6
        session_id = SessionManager.create_session(user_id)
        SessionManager.delete_session(session_id)
        self.assertNotIn(session_id, SessionManager.sessions)

if __name__ == "__main__":
    unittest.main()
