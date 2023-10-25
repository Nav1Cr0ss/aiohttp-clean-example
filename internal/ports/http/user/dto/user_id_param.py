from pydantic import BaseModel


class UserIdParam(BaseModel):
    id: int
