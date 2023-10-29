import asyncio
import concurrent.futures
from asyncio import Semaphore
from tempfile import NamedTemporaryFile

from aiohttp import StreamReader
from google.cloud import storage
from google.cloud.storage import Bucket as BucketGCP, Client as ClientGCP, Blob


class Bucket(BucketGCP):
    name = ""

    @classmethod
    def setup(cls, storage_client: ClientGCP) -> BucketGCP:
        return storage_client.bucket(cls.name)


class Storage:
    bucket: Bucket
    storage_client = None
    semaphore = Semaphore(2)

    def __init__(self):
        self._setup()

    def _setup(self):
        self.storage_client = storage.Client()
        self.bucket = self.bucket.setup(self.storage_client)

    async def _upload_file_by_stream(
        self, content: StreamReader, content_type: str, blob_name: str, chunk_size: int
    ) -> bool:
        try:
            blob = self.bucket.blob(blob_name)
            blob.content_type = content_type
            with blob.open("wb") as file_writer:
                async for chunk in content.iter_chunked(chunk_size):
                    file_writer.write(chunk)
            return True
        except Exception:
            print("some logging")
            return False

    def _upload_file_by_file_name(self, temp_filename: str, blob: Blob) -> bool:
        try:
            blob.upload_from_filename(temp_filename)
            return True
        except Exception:
            print("some logging")
            return False

    async def _upload_file_in_thread(
        self,
        content: StreamReader,
        content_type: str,
        blob_name: str,
    ) -> bool:
        try:
            async with self.semaphore:
                blob = self.bucket.blob(blob_name)
                blob.content_type = content_type

                temp_file = NamedTemporaryFile(delete=True)
                temp_file.write(await content.read())

                loop = asyncio.get_event_loop()
                executor = concurrent.futures.ThreadPoolExecutor()
                await loop.run_in_executor(
                    executor, self._upload_file_by_file_name, temp_file.name, blob
                )

            return True
        except Exception:
            print("Some logging")
            return False

    async def _download_file_to_bytes(self, blob_name: str) -> bytes:
        try:
            blob = self.bucket.blob(blob_name)
            contents = blob.download_as_string()
            return contents
        except Exception:
            print("some logging")
