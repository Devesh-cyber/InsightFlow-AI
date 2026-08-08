from datetime import datetime

from sqlmodel import SQLModel, Field


class Alert(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    dataset_id: int = Field(
        index=True,
    )

    snapshot_id: int = Field(
        index=True,
    )

    metric: str

    column: str | None = None

    old_value: float

    new_value: float

    percentage_change: float

    threshold: float

    direction: str

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )