from aiohttp.abc import Application
from aiohttp.web_routedef import RouteDef

from pkg.server.aiohttp.data import Route
from pkg.server.aiohttp.handler import HandlerFactory


class RouterFactory:
    hf = HandlerFactory

    @classmethod
    def get_compiled_routes(cls, routes: list[Route]) -> list[RouteDef]:
        return [cls.hf.build_handler(r) for r in routes]

    @classmethod
    def register_routes(cls, server: Application, routes: list[Route]):
        server.add_routes(cls.get_compiled_routes(routes))
