from datetime import datetime

from sqlmodel import Field, SQLModel


class Report(SQLModel, table=True):

    __tablename__ = "reports"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    dataset_id: int = Field(
        foreign_key="dataset.id",
        index=True,
    )

    report_type: str = Field(
        default="monitoring",
    )

    content: str

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )