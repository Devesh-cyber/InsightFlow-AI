from pathlib import Path
import shutil
from fastapi import HTTPException, UploadFile
from sqlmodel import Session, select
from app.models.dataset import Dataset
from app.services.snapshot_service import SnapshotService

class DatasetService:

    ALLOWED_EXTENSIONS = {
        'csv', 'xlsx'
    }

    def upload_dataset(self, session: Session, name: str, file: UploadFile):
        extension = file.filename.split('.')[-1].lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail='Unsupported file type'
            )

        upload_dir = Path('uploads')
        upload_dir.mkdir(exist_ok=True)
        file_path = upload_dir / file.filename

        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        dataset = session.exec(
            select(Dataset)
            .where(
                Dataset.name == name
            )
        ).first()
        
        if dataset is None:
            dataset = Dataset(
                name=name,
                filename=file.filename,
                file_path = str(file_path),
                extension=extension
            )

            session.add(dataset)
            session.commit()
            session.refresh(dataset)
        else:
            dataset.filename = file.filename
            dataset.file_path = str(file_path)
            dataset.extension = extension
            session.add(dataset)
            session.commit()
            session.refresh(dataset)

        SnapshotService().create_snapshot(
            session=session,
            dataset_id=dataset.id,
            file_path=str(file_path)
        )

        return dataset