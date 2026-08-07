from datetime import datetime
from sqlmodel import SQLModel


class DatasetResponse(SQLModel):

    id: int
    name: str
    filename: str
    extension: str
    created_at: datetime