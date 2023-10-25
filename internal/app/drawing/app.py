from typing import Optional

from aiohttp import StreamReader

from internal.adapters.client.ml_client.client import MLClient
from internal.adapters.repository.postgres.drawing.dto.create_file import CreateFileData
from internal.adapters.repository.repository import DrawingRepoIface
from internal.adapters.storage.gbacket.drawing_storage import StorageDrawing
from internal.app.app import DrawingAppIface
from internal.app.drawing.dto.file import DrawingFilter, FileListSchema, FileSchema
from internal.app.drawing.dto.file_history import DrawingHistoryFilter, FileHistoryListSchema, FileHistorySchema
from internal.domain.file import DrawingStatusEnum
from pkg.producer.dto.message import MsgPayload
from pkg.producer.producer import ProducerIface


class DrawingApp(DrawingAppIface):
    def __init__(
            self,
            repo: DrawingRepoIface,
            storage: StorageDrawing,
            producer: ProducerIface,
            ml_client: MLClient
    ):
        self.repo = repo
        self.storage = storage
        self.producer = producer
        self.ml_client = ml_client

    async def get_drawings(self, filters: DrawingFilter) -> FileListSchema:
        drawings = await self.repo.get_drawings(filters)
        return FileListSchema([FileSchema.model_validate(drawing) for drawing in drawings])

    async def get_drawings_history(self, filters: DrawingHistoryFilter) -> FileHistoryListSchema:
        drawings = await self.repo.get_drawings_history(filters)
        return FileHistoryListSchema([FileHistorySchema.model_validate(drawing) for drawing in drawings])

    async def get_drawing_history(self, drawing_id: int) -> FileHistoryListSchema:
        drawings = await self.get_drawings_history(DrawingHistoryFilter(file_id=drawing_id))
        return drawings

    async def upload_drawing(
            self,
            file_stream: StreamReader,
            content_type: str,
            file_name: str,
            user_id: int,
    ) -> Optional[int]:
        # The main idea is to upload drawings on internal storage as fast as we can and return user 200
        # And then in background we can continue with processing files, optimizations recognitions etc.

        is_uploaded = await self.storage.upload_drawing(file_stream, content_type, file_name)

        # On this step we already have file in our volumes,
        # so, we can return 203 and continue processing without holding request obj
        if not is_uploaded:
            return

        # It would be greate to create transaction here
        # The code above should work in background task,
        # technically we can use threads(or celery like)
        # but i would prefer background worker(something like cron job)
        file_id = await self.repo.create_file_data(
            CreateFileData(
                user_id=user_id,
                filename=file_name,
                status=DrawingStatusEnum.uploaded,
            )
        )
        # It is like in task requirements, but i would prefer using message queue instead direct call
        # above is alternative
        await self.ml_client.send_drawing_status(file_id, DrawingStatusEnum.uploaded)

        # just for example, it is not tested
        await self.producer.send(
            value=MsgPayload(
                payload={
                    "file_id": file_id,
                    "status": DrawingStatusEnum.uploaded,
                    "filename": file_name,
                }
            )
        )

        return file_id
