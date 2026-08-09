from datetime import datetime

from sqlmodel import Field, SQLModel


class Alert(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    dataset_id: int = Field(
        foreign_key="dataset.id",
        index=True,
    )

    snapshot_id: int = Field(
        foreign_key="snapshots.id",
        index=True,
    )

    column: str

    metric: str

    old_value: float

    new_value: float

    percentage_change: float

    threshold: float

    direction: str

    status: str = Field(
        default="active",
        index=True,
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )