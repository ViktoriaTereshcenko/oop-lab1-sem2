from jinja2 import Environment, FileSystemLoader
from http import cookies
from session import SessionManager
from logger import log_info

env = Environment(loader=FileSystemLoader("templates"))

# Тимчасово: username = admin, password = 1234
USERS = {
    "admin": {
        "password": "1234",
        "user_id": 1
    }
}

def login_get(request):
    template = env.get_template("login.html")
    content = template.render()

    request.send_response(200)
    request.send_header("Content-type", "text/html")
    request.end_headers()
    request.wfile.write(content.encode())


def login_post(request, params):
    username = params.get("username", [""])[0]
    password = params.get("password", [""])[0]

    user = USERS.get(username)
    if user and user["password"] == password:
        session_id = SessionManager.create_session(user["user_id"])
        c = cookies.SimpleCookie()
        c["session_id"] = session_id
        c["session_id"]["path"] = "/"
        request.send_response(302)
        request.send_header("Location", "/dashboard")
        request.send_header("Set-Cookie", c.output(header='', sep=''))
        request.end_headers()
        log_info(f"User '{username}' logged in")
    else:
        request.send_response(403)
        request.end_headers()
        request.wfile.write(b"Forbidden: Invalid credentials")
