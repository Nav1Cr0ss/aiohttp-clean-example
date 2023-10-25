from aiohttp import StreamReader

from pkg.storage.google_bucket.storage import Storage, Bucket
from settings import config

SIZE_10MB = 1024 * 1024 * 10


class BucketDrawing(Bucket):
    name = config.Storage.BUCKET_DRAWING


# I have decided to use gcp bucket because it can demonstrate the main idea without additional work
# In real scenario of this case, we should use local volumes which is attached to our pod
class StorageDrawing(Storage):
    bucket = BucketDrawing

    async def upload_drawing(self, file_stream: StreamReader, content_type: str, file_name: str) -> bool:
        return await self._upload_file_by_stream(
            content=file_stream,
            content_type=content_type,
            blob_name=file_name,
            chunk_size=SIZE_10MB,
        )
