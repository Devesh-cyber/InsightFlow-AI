from datetime import datetime

from sqlmodel import Field, SQLModel


class Snapshot(SQLModel, table=True):

    __tablename__ = "snapshots"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    dataset_id: int = Field(
        foreign_key="dataset.id",
        index=True,
    )

    version: int

    parquet_path: str

    dataset_hash: str

    rows: int

    columns: int

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )