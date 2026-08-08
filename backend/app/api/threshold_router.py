from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.config.database import get_session
from app.services.threshold_service import ThresholdService


router = APIRouter(
    prefix="/thresholds",
    tags=["Thresholds"],
)


service = ThresholdService()


@router.get(
    "/datasets/{dataset_id}"
)
def get_threshold(
    dataset_id: int,
    session: Session = Depends(get_session),
):

    return service.get_threshold(
        session=session,
        dataset_id=dataset_id,
    )


@router.put(
    "/datasets/{dataset_id}"
)
def update_threshold(
    dataset_id: int,
    threshold_percentage: float,
    session: Session = Depends(get_session),
):

    return service.set_threshold(
        session=session,
        dataset_id=dataset_id,
        threshold_percentage=threshold_percentage,
    )