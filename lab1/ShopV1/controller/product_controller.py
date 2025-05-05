from http import HTTPStatus
from template import render_template
from dao.product_dao import ProductDAO
from utils import redirect, parse_post_data, safe_int, check_access, logger

class ProductController:
    def __init__(self):
        self.product_dao = ProductDAO()

    def list_products(self, handler, session):
        products = self.product_dao.get_all_products()
        handler.send_response(HTTPStatus.OK)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(render_template('products/list.html', {'products': products}).encode())

    def create_form(self, handler, session):
        if not check_access(handler, role='admin'):
            return
        handler.send_response(HTTPStatus.OK)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(render_template('product_form.html').encode())

    def create(self, handler, session):
        if not check_access(handler, role='admin'):
            return
        data = parse_post_data(handler)
        name = data.get('name')
        description = data.get('description')
        price = safe_int(data.get('price'))

        if name and description and price is not None:
            self.product_dao.add_product(name, description, price)
            logger.info(f"Product '{name}' created by admin")
        else:
            logger.warning("Failed to create product due to invalid data")

        redirect(handler, '/products')

    def delete(self, handler, session, product_id=None):
        if not check_access(handler, role='admin'):
            return
        product_id = safe_int(product_id)
        if product_id is not None:
            self.product_dao.delete_product(product_id)
            logger.info(f"Product with ID {product_id} deleted by admin")
        else:
            logger.warning("Invalid product_id during delete")

        redirect(handler, '/products')
