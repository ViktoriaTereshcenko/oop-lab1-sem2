from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
from urllib.parse import urlparse
from router.router import Router
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
                handler(self, session)
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
                handler(self, session, params)
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
    from handlers.login import login_get, login_post
    from controllers.product_controller import ProductController

    product_controller = ProductController()

    Router.add_route("/login", "GET", login_get)
    Router.add_route("/login", "POST", login_post)

    Router.add_route("/products", "GET", product_controller.list_products)
    Router.add_route("/products/add", "GET", product_controller.create_form)
    Router.add_route("/products/add", "POST", product_controller.create)
    Router.add_route("/products/delete", "POST", product_controller.delete)

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

    run()
