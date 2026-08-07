from datetime import datetime
from sqlmodel import SQLModel

class SnapshotResponse(SQLModel):

    id: int
    dataset_id: int
    version: int
    rows: int
    columns: int
    created_at: datetime