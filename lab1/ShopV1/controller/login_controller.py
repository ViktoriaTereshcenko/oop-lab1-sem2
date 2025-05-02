from http import HTTPStatus
from http.cookies import SimpleCookie
from template import render_template
from session import SessionManager
from dao.user_dao import UserDAO
from utils import redirect, parse_post_data, logger

class LoginController:
    def __init__(self):
        self.user_dao = UserDAO()

    def login_form(self, handler):
        handler.send_response(HTTPStatus.OK)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(render_template('login.html').encode())

    def login(self, handler):
        data = parse_post_data(handler)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            logger.warning("Login attempt with empty username or password")
            return redirect(handler, '/login')

        user = self.user_dao.get_user_by_credentials(username, password)
        if user:
            session_id = SessionManager.create_session(user['id'])
            handler.send_response(HTTPStatus.SEE_OTHER)
            handler.send_header('Location', '/')
            cookie = SimpleCookie()
            cookie['session_id'] = session_id
            handler.send_header('Set-Cookie', cookie.output(header='', sep=''))
            handler.end_headers()
            logger.info(f"User '{username}' logged in successfully")
        else:
            logger.warning(f"Login failed for username '{username}'")
            redirect(handler, '/login')

    def logout(self, handler):
        cookie_header = handler.headers.get('Cookie')
        SessionManager.clear_session(cookie_header)
        logger.info("User logged out")
        redirect(handler, '/login')
