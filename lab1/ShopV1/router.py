from controllers.login_controller import LoginController
from controllers.blacklist_controller import BlacklistController
from controllers.user_controller import UserController

class Router:
    routes = {}

    @classmethod
    def initialize_routes(cls):
        login_controller = LoginController()
        user_controller = UserController()
        blacklist_controller = BlacklistController()

        cls.routes = {
            ('GET', '/login'): login_controller.login_form,
            ('POST', '/login'): login_controller.login,
            ('GET', '/logout'): login_controller.logout,
            ('GET', '/register'): user_controller.register_form,
            ('POST', '/register'): user_controller.register,
            ('GET', '/admin/users'): user_controller.list_users,
            ('GET', '/blacklist'): blacklist_controller.list_blacklist,
            ('POST', '/blacklist'): blacklist_controller.add_to_blacklist,
        }

    @classmethod
    def add_route(cls, path, method, handler):
        cls.routes[(method, path)] = handler

    @classmethod
    def get_handler(cls, path, method):
        return cls.routes.get((method, path))
