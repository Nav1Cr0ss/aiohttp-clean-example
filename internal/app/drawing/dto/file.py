from typing import Optional

from pydantic import RootModel, BaseModel

from internal.domain.file import File, DrawingStatusEnum
from pkg.pydantic_sqlalchemy.connector import sqlalchemy_to_pydantic

# Just for time saving. I don't recommend to use this in production. At least in this way


PydanticFile = sqlalchemy_to_pydantic(File)


class FileSchema(PydanticFile):
    class Config:
        from_attributes = True


class FileListSchema(RootModel):
    root: list[FileSchema]


class DrawingFilter(BaseModel):
    filename: Optional[str] = None
    user_id: Optional[int] = None
    status: Optional[DrawingStatusEnum] = None


