from pathlib import Path

import pandas as pd
from sqlmodel import Session, select

from app.engines.database_extraction_engine import (
    DatabaseExtractionEngine,
)
from app.models.data_source import DataSource
from app.models.snapshot import Snapshot
from app.utils.hash_utils import generate_dataframe_hash


class SnapshotService:

    def create_snapshot(
        self,
        session: Session,
        dataset_id: int,
        file_path: str,
    ) -> Snapshot:

        if file_path.endswith(".csv"):

            df = pd.read_csv(file_path)

        else:

            df = pd.read_excel(file_path)

        return self.create_snapshot_from_dataframe(
            session=session,
            dataset_id=dataset_id,
            df=df,
        )


    def create_snapshot_from_database(
        self,
        session: Session,
        dataset_id: int,
        data_source: DataSource,
    ) -> Snapshot | None:

        extraction_engine = (
            DatabaseExtractionEngine()
        )

        df = extraction_engine.extract(
            data_source=data_source
        )

        return self.create_snapshot_from_dataframe(
            session=session,
            dataset_id=dataset_id,
            df=df,
        )


    def create_snapshot_from_dataframe(
        self,
        session: Session,
        dataset_id: int,
        df: pd.DataFrame,
    ) -> Snapshot | None:

        dataset_hash = generate_dataframe_hash(df)

        latest = session.exec(
            select(Snapshot)
            .where(
                Snapshot.dataset_id == dataset_id
            )
            .order_by(
                Snapshot.version.desc()
            )
        ).first()

        # If the extracted data has not changed,
        # do not create another snapshot.
        if latest:

            if latest.dataset_hash == dataset_hash:

                return None

        version = 1

        if latest:

            version = latest.version + 1

        snapshot_directory = Path(
            f"snapshots/dataset_{dataset_id}"
        )

        snapshot_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        parquet_path = (
            snapshot_directory
            / f"v{version}.parquet"
        )

        df.to_parquet(
            parquet_path,
            index=False,
        )

        snapshot = Snapshot(
            dataset_id=dataset_id,
            version=version,
            parquet_path=str(parquet_path),
            dataset_hash=dataset_hash,
            rows=len(df),
            columns=len(df.columns),
        )

        session.add(snapshot)

        session.commit()

        session.refresh(snapshot)

        return snapshot