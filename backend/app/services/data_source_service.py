from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.data_source import DataSource


class DataSourceService:

    def create_data_source(
        self,
        session: Session,
        dataset_id: int,
        source_type: str,
        connection_string: str,
        table_name: str | None = None,
        query: str | None = None,
    ) -> DataSource:

        existing = session.exec(
            select(DataSource)
            .where(
                DataSource.dataset_id == dataset_id
            )
        ).first()

        if existing:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Data source already exists "
                    "for this dataset"
                ),
            )

        if not table_name and not query:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Either table_name or query "
                    "must be provided"
                ),
            )

        data_source = DataSource(
            dataset_id=dataset_id,
            source_type=source_type,
            connection_string=connection_string,
            table_name=table_name,
            query=query,
        )

        session.add(data_source)
        session.commit()
        session.refresh(data_source)

        return data_source


    def get_data_source(
        self,
        session: Session,
        dataset_id: int,
    ) -> DataSource:

        data_source = session.exec(
            select(DataSource)
            .where(
                DataSource.dataset_id == dataset_id
            )
        ).first()

        if not data_source:

            raise HTTPException(
                status_code=404,
                detail="Data source not found",
            )

        return data_source

    def update_data_source(
    self,
    session: Session,
    dataset_id: int,
    source_type: str,
    connection_string: str,
    table_name: str | None = None,
    query: str | None = None,
) -> DataSource:

        data_source = self.get_data_source(
            session=session,
            dataset_id=dataset_id,
        )

        if not table_name and not query:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Either table_name or query "
                    "must be provided"
                ),
            )

        data_source.source_type = source_type
        data_source.connection_string = connection_string
        data_source.table_name = table_name
        data_source.query = query

        session.add(data_source)
        session.commit()
        session.refresh(data_source)

        return data_source


def delete_data_source(
    self,
    session: Session,
    dataset_id: int,
) -> None:

    data_source = self.get_data_source(
        session=session,
        dataset_id=dataset_id,
    )

    session.delete(data_source)
    session.commit()