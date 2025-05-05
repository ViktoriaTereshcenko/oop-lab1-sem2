import unittest
from router import Router
from controllers.login_controller import LoginController
from controllers.register_controller import RegisterController
from controllers.index_controller import IndexController
from controllers.product_controller import ProductController
from controllers.user_controller import UserController
from controllers.order_controller import OrderController
from controllers.blacklist_controller import BlacklistController

class TestRouter(unittest.TestCase):
    def setUp(self):
        Router.routes.clear()

    def test_initialize_routes_populates_expected_paths(self):
        Router.initialize_routes()

        expected_routes = {
            ('GET', '/'),
            ('GET', '/index'),
            ('GET', '/login'),
            ('POST', '/login'),
            ('GET', '/logout'),
            ('GET', '/register'),
            ('POST', '/register'),
            ('GET', '/users'),
            ('GET', '/products'),
            ('GET', '/products/create'),
            ('POST', '/products/add'),
            ('POST', '/products/delete'),
            ('GET', '/orders'),
            ('GET', '/orders/create'),
            ('POST', '/orders/add'),
            ('POST', '/orders/pay'),
            ('GET', '/blacklist'),
            ('POST', '/blacklist'),
            ('POST', '/blacklist/remove'),
        }

        self.assertEqual(set(Router.routes.keys()), expected_routes)

        self.assertEqual(Router.routes[('GET', '/login')].__code__, LoginController().login_form.__code__)
        self.assertEqual(Router.routes[('POST', '/login')].__code__, LoginController().login.__code__)
        self.assertEqual(Router.routes[('GET', '/register')].__code__, RegisterController().register_form.__code__)
        self.assertEqual(Router.routes[('GET', '/index')].__code__, IndexController().index.__code__)
        self.assertEqual(Router.routes[('GET', '/products')].__code__, ProductController().list_products.__code__)
        self.assertEqual(Router.routes[('GET', '/users')].__code__, UserController().list_users.__code__)
        self.assertEqual(Router.routes[('GET', '/orders')].__code__, OrderController().list_orders.__code__)
        self.assertEqual(Router.routes[('GET', '/blacklist')].__code__, BlacklistController().list_blacklist.__code__)

    def test_add_route_and_get_handler(self):
        def dummy_handler():
            pass

        self.assertIsNone(Router.get_handler('/test', 'GET'))
        Router.routes[('GET', '/test')] = dummy_handler
        self.assertEqual(Router.get_handler('/test', 'GET'), dummy_handler)

    def test_get_handler_for_missing_route(self):
        Router.initialize_routes()
        self.assertIsNone(Router.get_handler('/nonexistent', 'GET'))
        self.assertIsNone(Router.get_handler('/login', 'PUT'))

if __name__ == "__main__":
    unittest.main()
