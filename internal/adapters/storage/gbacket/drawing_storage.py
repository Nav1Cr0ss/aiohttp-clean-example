from aiohttp import StreamReader, BodyPartReader

from pkg.storage.aio_google_bucket.storage import Storage
from settings import config


# I have decided to use gcp bucket because it can demonstrate the main idea without additional work
# In real scenario of this case, we should use local volumes which is attached to our pod
class StorageDrawing(Storage):
    bucket_name = config.Storage.BUCKET_DRAWING

    async def upload_drawing(
        self,
        file_stream: StreamReader | BodyPartReader,
        content_type: str,
        file_name: str,
    ) -> bool:
        return await self._upload_by_stream(
            content=file_stream,
            content_type=content_type,
            blob_name=file_name,
        )
