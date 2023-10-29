import asyncio
import logging

from aiohttp import web

from internal.adapters.client.ml_client.client import MLClient
from internal.adapters.producer.ml_client.producer import MlProducer
from internal.adapters.repository.postgres.drawing.repository import DrawingRepo
from internal.adapters.repository.postgres.user.repository import UserRepo
from internal.adapters.storage.gbacket.drawing_storage import StorageDrawing
from internal.app.drawing.app import DrawingApp
from internal.app.user.app import UserApp
from internal.ports.http.drawing.handler import DrawingHandler
from internal.ports.http.drawing.router import get_routes as get_drawing_routes
from internal.ports.http.user.handler import UserHandler
from internal.ports.http.user.router import get_routes as get_user_routes
from pkg.auth.dummy_provider.auth import DummyProvider
from pkg.db.postgres.postgres import Postgres
from pkg.server.aiohttp.router import RouterFactory
from settings import config


async def main():
    # db conn instance
    db = Postgres()

    # gcp bucket
    storage_drawing = StorageDrawing()

    # auth provider
    dummy_auth_provider = DummyProvider()

    # clients
    ml_client = MLClient(config.MLClient.BASE_URL)

    # producer
    ml_producer = MlProducer(config.KafkaBroker.BROKER_URL)

    # drawing repository
    drawing_repo = DrawingRepo(db)
    user_repo = UserRepo(db)

    # app layer
    drawing_app = DrawingApp(drawing_repo, storage_drawing, ml_producer, ml_client)
    user_app = UserApp(user_repo, dummy_auth_provider)

    # http layer
    drawing_handler = DrawingHandler(drawing_app)
    user_handler = UserHandler(user_app)

    # list of routes with adapter which helps with custom route level middlewares
    drawing_routes = get_drawing_routes(drawing_handler)
    user_routes = get_user_routes(user_handler)

    # aioHttp
    app = web.Application()
    logging.basicConfig(level=logging.INFO)

    # compile all handlers
    RouterFactory.register_routes(app, drawing_routes)
    RouterFactory.register_routes(app, user_routes)

    # server config
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, config.Server.HOST, config.Server.PORT)
    await site.start()

    await asyncio.sleep(100 * 3600)


if __name__ == "__main__":
    asyncio.run(main())
