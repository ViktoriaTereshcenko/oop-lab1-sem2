from http import HTTPStatus
from template import render_template
from dao.order_dao import OrderDAO
from dao.product_dao import ProductDAO
from utils import redirect, parse_post_data, check_access, safe_int, logger

class OrderController:
    def __init__(self):
        self.order_dao = OrderDAO()
        self.product_dao = ProductDAO()

    def list_orders(self, handler, session):
        user_id = check_access(handler)
        if not user_id:
            return
        orders = self.order_dao.get_orders_by_user(user_id)
        handler.send_response(HTTPStatus.OK)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(render_template('orders.html', {
            'orders': orders,
            'username': session.get('username', 'Користувач')
        }).encode())

    def create_form(self, handler, session):
        user_id = check_access(handler)
        if not user_id:
            return
        products = self.product_dao.get_all_products()
        handler.send_response(HTTPStatus.OK)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(render_template('order_form.html', {
            'products': products,
            'username': session.get('username', 'Користувач')
        }).encode())

    def create(self, handler, session):
        user_id = check_access(handler)
        if not user_id:
            return
        data = parse_post_data(handler)
        product_id = safe_int(data.get('product_id'))
        quantity = safe_int(data.get('quantity'))

        if product_id is not None and quantity is not None:
            self.order_dao.create_order(user_id, product_id, quantity)
            logger.info(f"User {user_id} created order for product {product_id}")
        else:
            logger.warning("Invalid product_id or quantity in order creation")

        redirect(handler, '/orders')

    def pay(self, handler, session, order_id):
        user_id = check_access(handler)
        if not user_id:
            return
        order_id = safe_int(order_id)
        if order_id is not None:
            self.order_dao.mark_order_paid(order_id)
            logger.info(f"User {user_id} paid for order {order_id}")
        else:
            logger.warning("Invalid order_id in payment")

        redirect(handler, '/orders')
