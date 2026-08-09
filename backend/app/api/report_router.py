from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.config.database import get_session

from app.schemas.report_schema import (
    ReportCreate,
    ReportResponse,
)

from app.services.report_service import (
    ReportService,
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.post(
    "/datasets/{dataset_id}",
    response_model=ReportResponse,
)
def generate_report(
    dataset_id: int,
    payload: ReportCreate,
    session: Session = Depends(get_session),
):

    service = ReportService()

    return service.generate_report(
        session=session,
        dataset_id=dataset_id,
        report_type=payload.report_type,
    )


@router.get(
    "/datasets/{dataset_id}",
    response_model=list[ReportResponse],
)
def get_dataset_reports(
    dataset_id: int,
    session: Session = Depends(get_session),
):

    service = ReportService()

    return service.get_dataset_reports(
        session=session,
        dataset_id=dataset_id,
    )


@router.get(
    "/{report_id}",
    response_model=ReportResponse,
)
def get_report(
    report_id: int,
    session: Session = Depends(get_session),
):

    service = ReportService()

    return service.get_report(
        session=session,
        report_id=report_id,
    )