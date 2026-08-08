from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.config.database import get_session
from app.services.monitoring_service import MonitoringService


router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"],
)


service = MonitoringService()


@router.get(
    "/datasets/{dataset_id}/compare"
)
def monitor_dataset(
    dataset_id: int,
    session: Session = Depends(get_session),
):

    return service.monitor_dataset(
        session=session,
        dataset_id=dataset_id,
    )