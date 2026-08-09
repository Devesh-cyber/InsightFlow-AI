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

    return service.get_dataset_alerts(
        session=session,
        dataset_id=dataset_id,
    )

@router.get("/datasets/{dataset_id}/active")
def get_active_alerts(
    dataset_id: int,
    session: Session = Depends(get_session)
):
    return service.get_active_alerts(
        session=session,
        dataset_id=dataset_id
    )


@router.put("/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    session: Session = Depends(get_session)
):
    return service.resolve_alert(
        session=session,
        alert_id=alert_id
    )