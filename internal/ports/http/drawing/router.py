from internal.ports.http.handler import DrawingHandlerIface
from pkg.server.aiohttp.data import Route
from pkg.server.aiohttp.methods import GET, POST

from pkg.server.aiohttp.middlewares.upload_pdf import upload_pdf


def get_routes(h: DrawingHandlerIface):
    routes = [
        Route("/drawings/upload", POST, h.upload_drawing, middlewares=(upload_pdf,)),
        Route("/drawings/history", GET, h.get_drawings_history, no_auth=True),
        # this route ive added for example, how useful can be such architecture
        Route("/drawings/{id}/history", GET, h.get_drawing_history, no_auth=True),
        Route("/drawings/", GET, h.get_drawings, no_auth=True),
    ]
    return routes
