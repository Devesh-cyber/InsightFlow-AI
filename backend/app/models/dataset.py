from datetime import datetime

from sqlmodel import SQLModel, Field


class Dataset(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    name: str
    filename: str
    file_path: str
    extension: str

    monitoring_enabled: bool = Field(
        default=True,
    )

    last_processed_snapshot_id: int | None = Field(
        default=None,
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )