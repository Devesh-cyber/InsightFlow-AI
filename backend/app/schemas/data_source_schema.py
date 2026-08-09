from pydantic import BaseModel


class DataSourceCreate(BaseModel):

    source_type: str

    connection_string: str

    table_name: str | None = None

    query: str | None = None


class DataSourceResponse(BaseModel):

    id: int

    dataset_id: int

    source_type: str

    table_name: str | None = None

    query: str | None = None