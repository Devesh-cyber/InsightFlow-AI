from pathlib import Path
import pandas as pd
from sqlmodel import Session, select
from app.models.snapshot import Snapshot
from app.utils.hash_utils import generate_dataframe_hash

class SnapshotService:

    def create_snapshot(self, session: Session, dataset_id: int, file_path: str):

        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)

        else:
            df = pd.read_excel(file_path)

        snapshot_directory = Path(
            f'snapshots/dataset_{dataset_id}'
        )
        snapshot_directory.mkdir(parents=True, exist_ok=True)

        latest = session.exec(
            select(Snapshot).
            where(Snapshot.dataset_id == dataset_id).
            order_by(Snapshot.version.desc())
        ).first()

        version = 1

        if latest:
            version = latest.version + 1

        parquet_path = (
            snapshot_directory / f"v{version}.parquet"
        )

        df.to_parquet(
            parquet_path,
            index=False
        )

        snapshot = Snapshot(
            dataset_id=dataset_id,
            version=version,
            parquet_path=str(parquet_path),
            dataset_hash=generate_dataframe_hash(df),
            rows=len(df),
            columns=len(df.columns)
        )

        session.add(snapshot)
        session.commit()
        session.refresh(snapshot)

        return snapshot