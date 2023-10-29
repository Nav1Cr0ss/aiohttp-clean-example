import base64
import hashlib
from typing import Optional

import jwt

from internal.app.user.dto.user import UserSchema
from pkg.auth.provider import AuthProviderIface
from pkg.server.aiohttp.errors import ErrUnauthorized
from settings import config


# Just for example, it isnt safe
class DummyProvider(AuthProviderIface):
    async def hash_password(self, raw_password: str) -> str:
        hashed_password = hashlib.pbkdf2_hmac(
            "sha256", raw_password.encode(), config.SECRET_KEY.encode(), 100000
        )
        return base64.b64encode(hashed_password).decode()

    async def auth_user(self, token: str) -> Optional[dict]:
        try:
            data = jwt.decode(
                token.split()[-1], config.SECRET_KEY, algorithms=["HS256"]
            )
            return data

        except IndexError:
            raise ErrUnauthorized("Authorization credentials were not found")
        except jwt.ExpiredSignatureError:
            raise ErrUnauthorized("Token has expired")
        except jwt.DecodeError:
            raise ErrUnauthorized("Token is invalid")

    async def get_credentials(self, user: UserSchema) -> str:
        token = jwt.encode(user.model_dump(), config.SECRET_KEY, algorithm="HS256")
        return token
