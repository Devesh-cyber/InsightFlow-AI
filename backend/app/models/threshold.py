from sqlmodel import SQLModel, Field


class DatasetThreshold(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True
    )
    dataset_id: int = Field(index=True)
    threshold_percentage: float = Field(
        default=10.0
    )