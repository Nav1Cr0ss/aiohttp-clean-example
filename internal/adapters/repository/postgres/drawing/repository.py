from typing import Optional

from sqlalchemy import insert, ScalarResult, select

from internal.adapters.repository.postgres.drawing.dto.create_file import CreateFileData
from internal.adapters.repository.repository import DrawingRepoIface
from internal.app.drawing.dto.file import DrawingFilter
from internal.app.drawing.dto.file_history import DrawingHistoryFilter
from internal.domain.file import File, FileHistory
from pkg.db.postgres.postgres import Postgres


class DrawingRepo(DrawingRepoIface):
    def __init__(self, db: Postgres):
        self.db = db

    async def get_drawing(self, drawing_id: int) -> Optional[File]:
        ...

    async def create_file_data(self, file_data: CreateFileData) -> int:
        stmt = insert(File).values(
            user_id=file_data.user_id,
            filename=file_data.filename,
            status=file_data.status
        )
        file_id = await self.db.insert(stmt)
        return file_id

    async def get_drawings(self, filters: DrawingFilter) -> ScalarResult[tuple[File]]:
        stmt = select(File)

        if filters.user_id is not None:
            stmt = stmt.where(File.user_id == filters.user_id)

        if filters.filename is not None:
            stmt = stmt.where(File.filename == filters.filename)

        if filters.status is not None:
            stmt = stmt.where(File.status == filters.status)
        drawings = await self.db.select(stmt)

        return drawings

    async def get_drawings_history(self, filters: DrawingHistoryFilter) -> ScalarResult[tuple[FileHistory]]:
        stmt = select(FileHistory)

        if filters.user_id is not None:
            stmt = stmt.where(FileHistory.user_id == filters.user_id)

        if filters.file_id is not None:
            stmt = stmt.where(FileHistory.file_id == filters.file_id)

        if filters.status is not None:
            stmt = stmt.where(FileHistory.status == filters.status)

        if filters.date_start is not None and filters.date_end is not None:
            stmt = stmt.where(FileHistory.timestamp.between(filters.date_start, filters.date_end))

        drawings = await self.db.select(stmt)

        return drawings
