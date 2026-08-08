from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.config.database import get_session
from app.services.alert_service import AlertService


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


service = AlertService()


@router.get(
    "/datasets/{dataset_id}"
)
def get_dataset_alerts(
    dataset_id: int,
    session: Session = Depends(
        get_session
    ),
):

    return service.get_alerts(
        session=session,
        dataset_id=dataset_id,
    )