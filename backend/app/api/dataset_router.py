from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlmodel import Session
from app.config.database import get_session
from app.schemas.dataset_schema import DatasetResponse
from app.services.dataset_service import DatasetService

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