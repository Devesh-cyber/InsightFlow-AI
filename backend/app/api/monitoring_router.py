from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.config.database import get_session
from app.services.monitoring_service import (
    MonitoringService
)
from app.schemas.monitoring_schema import MonitoringSummary
from app.services.alert_service import AlertService
from app.schemas.alert_schema import AlertResponse
from app.schemas.monitoring_schema import (
    SnapshotHistoryResponse,
)
from app.schemas.monitoring_schema import TimelineEvent
from app.schemas.monitoring_summary_schema import (
    MonitoringSummaryResponse,
)
from app.services.monitoring_summary_service import (
    MonitoringSummaryService,
)
from app.models.data_source import DataSource
from app.services.snapshot_service import SnapshotService



router = APIRouter (
    prefix = '/monitoring',
    tags=['Montioring']
)

service = MonitoringService()

@router.get(
    '/datasets/{dataset_id}/compare'
)
def monitor_dataset(
    dataset_id: int,
    session: Session = Depends(get_session)
):
    return service.monitor_dataset(
        session=session,
        dataset_id=dataset_id
    )

@router.get(
    "/datasets/{dataset_id}/summary",
    response_model=MonitoringSummaryResponse,
)
def get_monitoring_summary(
    dataset_id: int,
    session: Session = Depends(get_session),
):

    service = MonitoringSummaryService()

    summary = service.get_summary(
        session=session,
        dataset_id=dataset_id,
    )

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    return summary


@router.get(
    "/datasets/{dataset_id}/alerts",
    response_model=list[AlertResponse]
)
def get_dataset_alerts(
    dataset_id: int,
    status: str | None = None,
    session: Session = Depends(get_session),
):
    service = AlertService()

    return service.get_dataset_alerts(
        session=session,
        dataset_id=dataset_id,
        status=status,
    )

@router.get(
    "/datasets/{dataset_id}/snapshots",
    response_model=list[SnapshotHistoryResponse]
)
def get_snapshot_history(
    dataset_id: int,
    session: Session = Depends(get_session),
):
    service = MonitoringService()

    return service.get_snapshot_history(
        session=session,
        dataset_id=dataset_id,
    )

@router.get(
    "/datasets/{dataset_id}/timeline",
    response_model=list[TimelineEvent]
)
def get_monitoring_timeline(
    dataset_id: int,
    session: Session = Depends(get_session),
):
    service = MonitoringService()

    return service.get_monitoring_timeline(
        session=session,
        dataset_id=dataset_id,
    )

@router.post(
    "/datasets/{dataset_id}/snapshot/database"
)
def create_database_snapshot(
    dataset_id: int,
    session: Session = Depends(get_session),
):
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

    service = SnapshotService()

    return service.create_snapshot_from_database(
        session=session,
        dataset_id=dataset_id,
        data_source=data_source,
    )