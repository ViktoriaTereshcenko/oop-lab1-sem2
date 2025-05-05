from http import HTTPStatus
from template import render_template
from dao.blacklist_dao import BlacklistDAO
from utils import redirect, safe_int, parse_post_data, check_access, logger

class BlacklistController:
    def __init__(self):
        self.blacklist_dao = BlacklistDAO()

    def list_blacklist(self, handler, session):
        if not check_access(handler, role='admin'):
            return
        users = self.blacklist_dao.get_blacklist()
        handler.send_response(HTTPStatus.OK)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(render_template('blacklist.html', {
            'users': users,
            'username': session.get('username', 'Адміністратор')
        }).encode())

    def add_to_blacklist(self, handler, session):
        if not check_access(handler, role='admin'):
            return
        data = parse_post_data(handler)
        user_id = safe_int(data.get('user_id'))
        reason = data.get('reason', '')

        if user_id is not None:
            self.blacklist_dao.add_to_blacklist(user_id, reason)
            logger.info(f"User ID {user_id} added to blacklist")
        else:
            logger.warning("Invalid user_id when adding to blacklist")

        redirect(handler, '/blacklist')

    def remove_from_blacklist(self, handler, session, user_id):
        if not check_access(handler, role='admin'):
            return
        user_id = safe_int(user_id)
        if user_id is not None:
            self.blacklist_dao.remove_user_from_blacklist(user_id)
            logger.info(f"User ID {user_id} removed from blacklist")
        else:
            logger.warning("Invalid user_id when removing from blacklist")

        redirect(handler, '/blacklist')
