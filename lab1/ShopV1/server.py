from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from router.router import Router
from session import SessionManager
from logger import log_info, log_error

PORT = 8080

class CustomHandler(BaseHTTPRequestHandler):

    def do_get(self):
        handler = Router.get_handler(self.path, "GET")
        if handler:
            try:
                session = SessionManager.get_session_data(self.headers.get("Cookie"))
                handler(self, session)
            except Exception as e:
                log_error(str(e))
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Internal Server Error")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_post(self):
        handler = Router.get_handler(self.path, "POST")
        if handler:
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length).decode()
                params = parse_qs(post_data)
                session = SessionManager.get_session_data(self.headers.get("Cookie"))
                handler(self, session, params)
            except Exception as e:
                log_error(str(e))
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Internal Server Error")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

def run():
    httpd = HTTPServer(("", PORT), CustomHandler)
    log_info(f"Server running at http://localhost:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":

    def dashboard(request, session):
        if not session:
            request.send_response(302)
            request.send_header("Location", "/login")
            request.end_headers()
            return
        request.send_response(200)
        request.end_headers()
        user_id = session["user_id"]
        request.wfile.write(f"Welcome, user {user_id}!".encode())

    Router.add_route("/dashboard", "GET", dashboard)
