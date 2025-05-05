import uuid
from http import cookies

class SessionManager:
    sessions = {}

    @staticmethod
    def create_session(user_id, role="client"):
        session_id = str(uuid.uuid4())
        SessionManager.sessions[session_id] = {"user_id": user_id, "role": role}
        return session_id

    @staticmethod
    def get_session_data(cookie_header):
        if not cookie_header:
            return None
        c = cookies.SimpleCookie()
        c.load(cookie_header)
        session_cookie = c.get("session_id")
        if session_cookie and session_cookie.value in SessionManager.sessions:
            return SessionManager.sessions[session_cookie.value]
        return None

    @staticmethod
    def get_session_user_id(cookie_header):
        session_data = SessionManager.get_session_data(cookie_header)
        if session_data:
            return session_data.get("user_id")
        return None

    @staticmethod
    def clear_session(cookie_header):
        if not cookie_header:
            return
        c = cookies.SimpleCookie()
        c.load(cookie_header)
        session_cookie = c.get("session_id")
        if session_cookie and session_cookie.value in SessionManager.sessions:
            del SessionManager.sessions[session_cookie.value]

    @staticmethod
    def set_user_role(user_id, role):
        for sid, data in SessionManager.sessions.items():
            if data["user_id"] == user_id:
                data["role"] = role

    @staticmethod
    def delete_session(session_id):
        SessionManager.sessions.pop(session_id, None)
