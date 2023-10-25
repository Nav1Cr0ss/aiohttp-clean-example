from pydantic import BaseModel


class DrawingIdParam(BaseModel):
    id: int
