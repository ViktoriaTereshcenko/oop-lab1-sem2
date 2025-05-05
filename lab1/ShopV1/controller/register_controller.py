from http import HTTPStatus
from template import render_template
from session import SessionManager
from dao.user_dao import UserDAO
from utils import logger

class RegisterController:
    def __init__(self):
        self.user_dao = UserDAO()

    @staticmethod
    def register_form(handler, session):
        handler.send_response(HTTPStatus.OK)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(render_template('register.html').encode())

    def register(self, handler, session, params):
        username = params.get('username')
        password = params.get('password')

        if not username or not password:
            handler.send_response(HTTPStatus.OK)
            handler.send_header('Content-type', 'text/html')
            handler.end_headers()
            handler.wfile.write(render_template('register.html', {
                'error': 'All fields are required.'
            }).encode())
            return

        try:
            self.user_dao.create_user(username, password, role='user')
            logger.info(f"User '{username}' successfully registered.")

            user = self.user_dao.get_user_by_credentials(username, password)
            session_id = SessionManager.create_session(user['id'])

            handler.send_response(HTTPStatus.SEE_OTHER)
            handler.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly')
            handler.send_header('Location', '/')
            handler.end_headers()
        except Exception as e:
            logger.warning(f"Failed to register user '{username}': {e}")
            handler.send_response(HTTPStatus.OK)
            handler.send_header('Content-type', 'text/html')
            handler.end_headers()
            handler.wfile.write(render_template('register.html', {
                'error': f"User '{username}' already exists or an error occurred."
            }).encode())
