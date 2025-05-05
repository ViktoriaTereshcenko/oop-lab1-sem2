from controllers.login_controller import LoginController
from controllers.register_controller import RegisterController
from controllers.index_controller import IndexController
from controllers.product_controller import ProductController
from controllers.user_controller import UserController
from controllers.order_controller import OrderController
from controllers.blacklist_controller import BlacklistController

class Router:
    routes = {}

    @staticmethod
    def initialize_routes():
        login_controller = LoginController()
        register_controller = RegisterController()
        index_controller = IndexController()
        product_controller = ProductController()
        user_controller = UserController()
        order_controller = OrderController()
        blacklist_controller = BlacklistController()

        Router.routes = {
            # Головна
            ('GET', '/'): lambda handler, session: Router.redirect_to_login(handler),
            ('GET', '/index'): index_controller.index,

            # Аутентифікація
            ('GET', '/login'): login_controller.login_form,
            ('POST', '/login'): login_controller.login,
            ('GET', '/logout'): login_controller.logout,

            # Реєстрація
            ('GET', '/register'): register_controller.register_form,
            ('POST', '/register'): register_controller.register,

            # Користувачі
            ('GET', '/users'): user_controller.list_users,

            # Продукти
            ('GET', '/products'): product_controller.list_products,
            ('GET', '/products/create'): product_controller.create_form,
            ('POST', '/products/add'): product_controller.create,
            ('POST', '/products/delete'): product_controller.delete,

            # Замовлення
            ('GET', '/orders'): order_controller.list_orders,
            ('GET', '/orders/create'): order_controller.create_form,
            ('POST', '/orders/add'): order_controller.create,
            ('POST', '/orders/pay'): order_controller.pay,

            # Чорний список
            ('GET', '/blacklist'): blacklist_controller.list_blacklist,
            ('POST', '/blacklist'): blacklist_controller.add_to_blacklist,
            ('POST', '/blacklist/remove'): blacklist_controller.remove_from_blacklist,
        }

    @staticmethod
    def get_handler(path, method):
        return Router.routes.get((method, path))

    @staticmethod
    def redirect_to_login(handler):
        from utils import redirect
        redirect(handler, '/login')
