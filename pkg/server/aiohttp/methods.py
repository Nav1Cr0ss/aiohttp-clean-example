from aiohttp import web

from pkg.server.aiohttp.data import Method

GET: Method = web.get
POST: Method = web.post
PATCH: Method = web.patch
