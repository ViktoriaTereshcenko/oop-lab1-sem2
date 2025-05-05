from http import HTTPStatus
from template import render_template
from dao.user_dao import UserDAO
from utils import check_access

class IndexController:
    @staticmethod
    def index(handler, session):
        user_id = check_access(handler)
        if user_id is None:
            return

        user = UserDAO().get_user_by_id(user_id)
        username = user.get('username') if user else 'Користувач'

        handler.send_response(HTTPStatus.OK)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(render_template('index.html', {'username': username}).encode())
