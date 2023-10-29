import enum
from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from internal.domain.account import User
from pkg.orm.models.base import Base


class DrawingStatusEnum(enum.StrEnum):
    uploaded = "uploaded"
    pending = "pending"
    processed = "processed"


class File(Base):
    __tablename__ = "drawing_files"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("account_users.id"))
    user: Mapped[User] = relationship()
    filename: Mapped[str] = mapped_column(String(255))
    status: Mapped[DrawingStatusEnum]

    def __repr__(self) -> str:
        return self.filename


class FileHistory(Base):
    __tablename__ = "drawing_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    file_id = mapped_column(ForeignKey("drawing_files.id"))
    file: Mapped[File] = relationship()
    user_id = mapped_column(ForeignKey("account_users.id"))
    user: Mapped[User] = relationship()
    timestamp: Mapped[datetime]
    status: Mapped[DrawingStatusEnum]

    def __repr__(self) -> str:
        return self.status
