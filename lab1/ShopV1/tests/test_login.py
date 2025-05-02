import unittest
from io import BytesIO
from http import cookies
import session
import login_handler

class DummyRequest:
    def __init__(self):
        self._status = None
        self._headers = {}
        self.wfile = BytesIO()

    def send_response(self, code):
        self._status = code

    def send_header(self, key, value):
        self._headers[key] = value

    def end_headers(self):
        pass

class TestLoginHandler(unittest.TestCase):
    def setUp(self):
        session.sessions.clear()
        class DummyTemplate:
            def render(self):
                return "<form>Login</form>"
        login_handler.env.loader = None
        login_handler.env.get_template = lambda name: DummyTemplate()

    def test_login_get(self):
        req = DummyRequest()
        login_handler.login_get(req)
        self.assertEqual(req._status, 200)
        self.assertIn("Content-type", req._headers)
        self.assertEqual(req._headers["Content-type"], "text/html")
        body = req.wfile.getvalue().decode()
        self.assertIn("<form>Login</form>", body)

    def test_login_post_success(self):
        req = DummyRequest()
        params = {"username": ["admin"], "password": ["1234"]}
        login_handler.login_post(req, params)

        self.assertEqual(req._status, 302)
        self.assertEqual(req._headers.get("Location"), "/dashboard")
        set_cookie = req._headers.get("Set-Cookie")
        self.assertIsNotNone(set_cookie)
        c = cookies.SimpleCookie()
        c.load(set_cookie)
        self.assertIn("session_id", c)
        sid = c["session_id"].value
        self.assertIn(sid, session.sessions)
        self.assertEqual(session.sessions[sid]["user_id"], 1)

    def test_login_post_failure(self):
        req = DummyRequest()
        params = {"username": ["admin"], "password": ["wrong"]}
        login_handler.login_post(req, params)
        self.assertEqual(req._status, 403)
        body = req.wfile.getvalue()
        self.assertEqual(body, b"Forbidden: Invalid credentials")
        self.assertEqual(len(session.sessions), 0)

    def test_login_post_unknown_user(self):
        req = DummyRequest()
        params = {"username": ["noone"], "password": ["whatever"]}
        login_handler.login_post(req, params)
        self.assertEqual(req._status, 403)
        body = req.wfile.getvalue()
        self.assertEqual(body, b"Forbidden: Invalid credentials")

if __name__ == "__main__":
    unittest.main()
