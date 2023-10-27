__all__ = ["Storage"]

import io
from asyncio import Semaphore

import aiohttp
from aiohttp import StreamReader, BodyPartReader
from gcloud.aio.storage import Storage as AIOStorage


class Storage(AIOStorage):
    bucket_name = ""
    semaphore = Semaphore(10)

    async def __upload(
            self,
            file_data: io.BytesIO,
            content_type: str,
            blob_name: str,
    ) -> bool:
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession() as session:
                    status = await self.upload(
                        bucket=self.bucket_name,
                        session=session,
                        content_type=content_type,
                        file_data=file_data,
                        object_name=blob_name,

                    )
                    return bool(status.get("id"))
        except Exception as exc:
            print("some logging")
            return False

    async def _upload_by_stream(
            self,
            content: StreamReader | BodyPartReader,
            content_type: str,
            blob_name: str,
    ):

        return await self.__upload(
            file_data=io.BytesIO(await content.read()),
            content_type=content_type,
            blob_name=blob_name,
        )
