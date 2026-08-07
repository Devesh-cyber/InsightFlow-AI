from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Snapshot(SQLModel, table=True):

    __tablename__ = 'snapshots'
    id: Optional[int] = Field(None, primary_key=True)
    dataset_id: int = Field(foreign_key='datasets.id')
    version: int
    parquet_path: str
    dataset_hash: str
    rows: int
    columns: int
    created_at: datetime = Field(default_factory=datetime.now)

