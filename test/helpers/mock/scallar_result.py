from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class MockScalarResult(Generic[T]):
    def __init__(self, result: tuple[T]):
        self._result = result

    async def fetch(self) -> tuple[T]:
        return self._result

    def one_or_none(self) -> Optional[T]:
        if self._result:
            return self._result[0]
