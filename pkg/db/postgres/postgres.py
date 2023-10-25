from typing import TypeVar, Optional

from sqlalchemy import Select, ScalarResult, Insert, Update


from pkg.db.postgres.session import async_session

T = TypeVar("T")


class Postgres:
    session = async_session

    @classmethod
    async def select_one_or_none(cls, stmt: Select[T]) -> Optional[T]:
        async with cls.session() as session:
            result = await session.scalars(stmt)
            return result.one_or_none()

    @classmethod
    async def select(cls, stmt: Select[T]) -> ScalarResult[T]:
        async with cls.session() as session:
            result = await session.scalars(stmt)
            return result

    @classmethod
    async def insert(cls, stmt: Insert[T]) -> int:
        async with cls.session() as session:
            result = await session.execute(stmt)
            await session.commit()
            return int(result.inserted_primary_key[0])

    @classmethod
    async def update(cls, stmt: Update[T]) -> None:
        async with cls.session() as session:
            await session.execute(stmt)
            await session.commit()
