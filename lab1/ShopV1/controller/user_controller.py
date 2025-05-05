from http import HTTPStatus
from template import render_template
from dao.user_dao import UserDAO
from utils import redirect, parse_post_data, check_access, logger

class UserController:
    def __init__(self):
        self.user_dao = UserDAO()

    def list_users(self, handler):
        if not check_access(handler, role='admin'):
            return
        users = self.user_dao.get_all_users()
        handler.send_response(HTTPStatus.OK)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(render_template('users.html', {'users': users}).encode())

    @staticmethod
    def register_form(handler):
        handler.send_response(HTTPStatus.OK)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(render_template('register.html').encode())

    def register(self, handler):
        data = parse_post_data(handler)
        username = data.get('username')
        password = data.get('password')

        if username and password:
            self.user_dao.create_user(username, password)
            logger.info(f"User '{username}' registered")
            redirect(handler, '/login')
        else:
            logger.warning("Registration failed due to missing username or password")
            redirect(handler, '/register')
