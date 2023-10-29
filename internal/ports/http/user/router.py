from internal.ports.http.handler import UserHandlerIface
from pkg.server.aiohttp.data import Route
from pkg.server.aiohttp.methods import POST, GET, PATCH
from pkg.server.aiohttp.middlewares.construct_request_body import construct_request_body


def get_routes(h: UserHandlerIface):
    routes = [
        Route("/users", GET, h.get_users),
        Route(
            "/users/{id}",
            PATCH,
            h.partial_update_user,
            middlewares=(construct_request_body,),
        ),
        Route(
            "/users/register",
            POST,
            h.create_user,
            no_auth=True,
            middlewares=(construct_request_body,),
        ),
        Route(
            "/users/login",
            POST,
            h.login_user,
            no_auth=True,
            middlewares=(construct_request_body,),
        ),
    ]
    return routes
