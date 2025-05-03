import unittest
from controllers.login_controller import LoginController
from controllers.blacklist_controller import BlacklistController
from controllers.user_controller import UserController
from router import Router

class TestRouter(unittest.TestCase):
    def setUp(self):
        Router.routes.clear()

    def test_initialize_routes_populates_expected_paths(self):
        Router.initialize_routes()
        expected_keys = {
            ('GET', '/'),
            ('GET', '/login'),
            ('POST', '/login'),
            ('GET', '/logout'),
            ('GET', '/register'),
            ('POST', '/register'),
            ('GET', '/admin/users'),
            ('GET', '/blacklist'),
            ('POST', '/blacklist'),
            ('GET', '/products'),
            ('GET', '/products/create'),
            ('POST', '/products/create'),
            ('POST', '/products/delete'),
        }

        self.assertEqual(set(Router.routes.keys()), expected_keys)

        self.assertTrue(callable(Router.routes[('GET', '/login')]))
        self.assertIsInstance(Router.routes[('GET', '/login')].__self__, LoginController)

        self.assertTrue(callable(Router.routes[('GET', '/blacklist')]))
        self.assertIsInstance(Router.routes[('GET', '/blacklist')].__self__, BlacklistController)

        self.assertTrue(callable(Router.routes[('GET', '/register')]))
        self.assertIsInstance(Router.routes[('GET', '/register')].__self__, UserController)

    def test_add_route_and_get_handler(self):
        def dummy_handler():
            pass

        self.assertIsNone(Router.get_handler('/test', 'GET'))

        Router.add_route('/test', 'GET', dummy_handler)
        handler = Router.get_handler('/test', 'GET')
        self.assertIs(handler, dummy_handler)

    def test_get_handler_for_missing_route(self):
        Router.initialize_routes()
        self.assertIsNone(Router.get_handler('/doesnotexist', 'GET'))
        self.assertIsNone(Router.get_handler('/login', 'PUT'))

if __name__ == "__main__":
    unittest.main()
