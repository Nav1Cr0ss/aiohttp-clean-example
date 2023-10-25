from dataclasses import dataclass
from internal.domain.file import DrawingStatusEnum


@dataclass
class CreateFileData:
    user_id: int
    filename: str
    status: DrawingStatusEnum
