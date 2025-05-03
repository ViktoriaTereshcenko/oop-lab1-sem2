from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
from urllib.parse import urlparse
from router import Router
from session import SessionManager
from logger import log_info, log_error
from utils import parse_post_data

PORT = 8080

class CustomHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        handler = Router.get_handler(parsed_path.path, "GET")
        if handler:
            try:
                session = SessionManager.get_session_data(self.headers.get("Cookie"))
                if handler.__code__.co_argcount == 2:
                    handler(self, session)
                else:
                    handler(self)
            except Exception as e:
                log_error(f"GET {self.path} failed: {str(e)}")
                self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
                self.end_headers()
                self.wfile.write(b"Internal Server Error")
        else:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        parsed_path = urlparse(self.path)
        handler = Router.get_handler(parsed_path.path, "POST")
        if handler:
            try:
                session = SessionManager.get_session_data(self.headers.get("Cookie"))
                params = parse_post_data(self)
                if handler.__code__.co_argcount == 3:
                    handler(self, session, params)
                else:
                    handler(self)
            except Exception as e:
                log_error(f"POST {self.path} failed: {str(e)}")
                self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
                self.end_headers()
                self.wfile.write(b"Internal Server Error")
        else:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()
            self.wfile.write(b"404 Not Found")


def run():
    httpd = HTTPServer(("", PORT), CustomHandler)
    log_info(f"Server running at http://localhost:{PORT}")
    httpd.serve_forever()


if __name__ == "__main__":
    Router.initialize_routes()
    run()
