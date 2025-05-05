from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
from urllib.parse import urlparse
from router import Router
from session import SessionManager
from logger import log_info, log_error
from utils import parse_post_data
import traceback

PORT = 8080

class CustomHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        handler = Router.get_handler(parsed_path.path, "GET")
        if handler:
            try:
                session = SessionManager.get_session_data(self.headers.get("Cookie"))
                arg_count = handler.__code__.co_argcount
                if arg_count == 3:
                    handler(self, session)
                elif arg_count == 2:
                    handler(self, session)
                elif arg_count == 1:
                    handler(self)
                else:
                    raise TypeError("Unsupported number of arguments for handler")
            except Exception as e:
                log_error(f"GET {self.path} failed:\n" + traceback.format_exc())
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
                arg_count = handler.__code__.co_argcount
                if arg_count == 3:
                    handler(self, session, params)
                elif arg_count == 2:
                    handler(self, session)
                elif arg_count == 1:
                    handler(self)
                else:
                    raise TypeError("Unsupported number of arguments for handler")
            except Exception as e:
                log_error(f"POST {self.path} failed:\n" + traceback.format_exc())
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
