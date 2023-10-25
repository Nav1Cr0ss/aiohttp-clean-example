from aiohttp import StreamReader
from google.cloud import storage
from google.cloud.storage import Bucket as BucketGCP, Client as ClientGCP


class Bucket(BucketGCP):
    name = ""

    @classmethod
    def setup(cls, storage_client: ClientGCP) -> BucketGCP:
        return storage_client.bucket(cls.name)


class Storage:
    bucket: Bucket
    storage_client = None

    def __init__(self):
        self._setup()

    def _setup(self):
        self.storage_client = storage.Client()
        self.bucket = self.bucket.setup(self.storage_client)

    async def _upload_file_by_name(self, file_name: str, blob_name: str):
        try:
            blob = self.bucket.blob(blob_name)
            blob.upload_from_filename(file_name)
        except Exception:
            print("some logging")

    async def _upload_file_by_bytes(self, file_bytes: bytes, blob_name: str) -> str:
        try:
            blob = self.bucket.blob(blob_name)
            blob.upload_from_string(file_bytes)
            return blob_name
        except Exception as exc:
            print("some logging")

    async def _upload_file_by_stream(
            self,
            content: StreamReader,
            content_type: str,
            blob_name: str,
            chunk_size: int) -> bool:
        try:
            blob = self.bucket.blob(blob_name)
            blob.content_type = content_type
            with blob.open('wb') as file_writer:
                async for chunk in content.iter_chunked(chunk_size):
                    file_writer.write(chunk)
            return True
        except Exception as exc:
            print("some logging")
            return False

    async def _download_file_to_bytes(self, blob_name: str) -> bytes:
        try:
            blob = self.bucket.blob(blob_name)
            contents = blob.download_as_string()
            return contents
        except Exception as exc:
            print("some logging")
