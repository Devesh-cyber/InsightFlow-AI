from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlmodel import Session
from app.config.database import get_session
from app.schemas.dataset_schema import DatasetResponse
from app.services.dataset_service import DatasetService
from app.models.dataset import Dataset

router = APIRouter(
    prefix='/dataset',
    tags=['Datasets']
)

service = DatasetService()

@router.post(
    '/upload',
    response_model=DatasetResponse
)
def upload_dataset(
    name: str = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    return service.upload_dataset(
        session=session, name=name, file=file
    )

@router.put(
    "/{dataset_id}/monitoring"
)
def update_monitoring(
    dataset_id: int,
    enabled: bool,
    session: Session = Depends(
        get_session
    ),
):

    dataset = session.get(
        Dataset,
        dataset_id,
    )

    if dataset is None:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    dataset.monitoring_enabled = enabled

    session.add(dataset)

    session.commit()

    session.refresh(dataset)

    return {
        "dataset_id": dataset.id,
        "monitoring_enabled": (
            dataset.monitoring_enabled
        ),
    }