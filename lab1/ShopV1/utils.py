import logging
from urllib.parse import parse_qs
from http import HTTPStatus
from session import SessionManager
from dao.user_dao import UserDAO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def redirect(handler, location):
    handler.send_response(HTTPStatus.SEE_OTHER)
    handler.send_header('Location', location)
    handler.end_headers()

def parse_post_data(handler):
    content_length = int(handler.headers.get('Content-Length', 0))
    post_data = handler.rfile.read(content_length).decode()
    return {k: v[0] for k, v in parse_qs(post_data).items()}

def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

def check_access(handler, role=None):
    cookie_header = handler.headers.get('Cookie')
    user_id = SessionManager.get_session_user_id(cookie_header)

    if user_id is None:
        logger.warning("Access denied: no session")
        redirect(handler, '/login')
        return None

    user_dao = UserDAO()
    user = user_dao.get_user_by_id(user_id)

    if not user:
        logger.warning("Access denied: user not found")
        redirect(handler, '/login')
        return None

    if role and user.get('role') != role:
        logger.warning(f"Access denied: role mismatch (required={role}, actual={user.get('role')})")
        redirect(handler, '/login')
        return None

    return user_id
