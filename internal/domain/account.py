import enum

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from pkg.orm.models.base import Base


class RoleEnum(enum.StrEnum):
    admin = "admin"
    staff = "staff"


class User(Base):
    __tablename__ = "account_users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150))
    password_hash: Mapped[str] = mapped_column(String(150))
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum))

    def __repr__(self) -> str:
        return self.username
