from typing import Optional

from sqlmodel import Field, SQLModel


class DataSource(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )

    dataset_id: int = Field(
        foreign_key="dataset.id",
        index=True,
    )

    source_type: str

    connection_string: str

    table_name: str | None = None

    query: str | None = None