from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class Alert(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    dataset_id: int = Field(
        foreign_key="dataset.id"
    )

    snapshot_id: int = Field(
        foreign_key="snapshots.id"
    )

    column: str

    metric: str

    old_value: float

    new_value: float

    percentage_change: float

    threshold: float

    direction: str

    status: str = Field(
        default="active"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )