from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.config.database import get_session
from app.schemas.data_source_schema import (
    DataSourceCreate,
    DataSourceResponse,
)
from app.services.data_source_service import (
    DataSourceService,
)


router = APIRouter(
    prefix="/data-sources",
    tags=["Data Sources"],
)


@router.post(
    "/datasets/{dataset_id}",
    response_model=DataSourceResponse,
)
def create_data_source(
    dataset_id: int,
    payload: DataSourceCreate,
    session: Session = Depends(get_session),
):

    service = DataSourceService()

    return service.create_data_source(
        session=session,
        dataset_id=dataset_id,
        source_type=payload.source_type,
        connection_string=payload.connection_string,
        table_name=payload.table_name,
    )


@router.get(
    "/datasets/{dataset_id}",
    response_model=DataSourceResponse,
)
def get_data_source(
    dataset_id: int,
    session: Session = Depends(get_session),
):

    service = DataSourceService()

    return service.get_data_source(
        session=session,
        dataset_id=dataset_id,
    )