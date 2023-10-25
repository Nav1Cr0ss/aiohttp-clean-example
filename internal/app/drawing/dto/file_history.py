from datetime import datetime
from typing import Optional

from pydantic import RootModel, BaseModel
from internal.domain.file import FileHistory, DrawingStatusEnum
from pkg.pydantic_sqlalchemy.connector import sqlalchemy_to_pydantic

PydanticFileHistory = sqlalchemy_to_pydantic(FileHistory)


class FileHistorySchema(PydanticFileHistory):
    class Config:
        from_attributes = True


class FileHistoryListSchema(RootModel):
    root: list[FileHistorySchema]


class DrawingHistoryFilter(BaseModel):
    file_id: Optional[int] = None
    user_id: Optional[int] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    status: Optional[DrawingStatusEnum] = None
