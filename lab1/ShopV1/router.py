from controllers.login_controller import LoginController
from controllers.blacklist_controller import BlacklistController
from controllers.user_controller import UserController
from controllers.product_controller import ProductController

class Router:
    routes = {}

    @classmethod
    def initialize_routes(cls):
        login_controller     = LoginController()
        user_controller      = UserController()
        blacklist_controller = BlacklistController()
        product_controller   = ProductController()

        cls.routes = {
            ('GET',    '/login'):       login_controller.login_form,
            ('POST',   '/login'):       login_controller.login,
            ('GET',    '/logout'):      login_controller.logout,
            ('GET',    '/register'):    user_controller.register_form,
            ('POST',   '/register'):    user_controller.register,
            ('GET',    '/admin/users'): user_controller.list_users,
            ('GET',    '/blacklist'):   blacklist_controller.list_blacklist,
            ('POST',   '/blacklist'):   blacklist_controller.add_to_blacklist,
            ('GET',    '/'):                      product_controller.list_products,
            ('GET',    '/products'):              product_controller.list_products,
            ('GET',    '/products/create'):       product_controller.create_form,
            ('POST',   '/products/create'):       product_controller.create,
            ('POST',   '/products/delete'):       product_controller.delete,
        }

    @classmethod
    def add_route(cls, path, method, handler):
        cls.routes[(method, path)] = handler

    @classmethod
    def get_handler(cls, path, method):
        return cls.routes.get((method, path))
