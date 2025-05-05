from http import HTTPStatus
from template import render_template
from session import SessionManager
from dao.user_dao import UserDAO
from utils import redirect, logger

class LoginController:
    def __init__(self):
        self.user_dao = UserDAO()

    @staticmethod
    def login_form(handler, session):
        handler.send_response(HTTPStatus.OK)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(render_template('login.html').encode())

    def login(self, handler, session, params):
        username = params.get('username')
        password = params.get('password')

        if not username or not password:
            logger.warning("Login attempt with empty username or password")
            redirect(handler, '/login')
            return

        user = self.user_dao.get_user_by_credentials(username, password)
        if user:
            session_id = SessionManager.create_session(user['id'])

            handler.send_response(HTTPStatus.SEE_OTHER)
            handler.send_header('Location', '/')
            handler.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly')
            handler.end_headers()

            logger.info(f"User '{username}' logged in successfully")
        else:
            logger.warning(f"Login failed for username '{username}'")
            redirect(handler, '/login')
            return

    @staticmethod
    def logout(handler, session):
        cookie_header = handler.headers.get('Cookie')
        SessionManager.clear_session(cookie_header)
        logger.info("User logged out")
        redirect(handler, '/login')
        return
