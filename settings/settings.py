__ALL__ = ["Settings"]

from decouple import config


class Storage:
    BUCKET_DRAWING: str = config('BUCKET_DRAWING')


class DB:
    DATABASE: str = config('DB_DATABASE')
    HOST: str = config('DB_HOST')
    PASSWORD: str = config('DB_PASSWORD')
    PORT: int = config('DB_PORT')
    USER: str = config('DB_USER')


class Postgres(DB):
    def get_conn_string(self) -> str:
        db_url = f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"
        return db_url


class Server:
    HOST: str = config('HOST')
    PORT: int = config('PORT')


class MLClient:
    BASE_URL: str = config('ML_CLIENT_BASE_URL')


class KafkaBroker:
    BROKER_URL: str = config('KAFKA_BROKER_URL')


class Settings:
    DB: Postgres = Postgres()
    Server: Server = Server()
    Storage: Storage = Storage()
    MLClient: MLClient = MLClient()
    KafkaBroker: KafkaBroker = KafkaBroker()
    DEBUG: bool = config('DEBUG', default=False, cast=bool)
    SECRET_KEY: str = config('SECRET_KEY')
