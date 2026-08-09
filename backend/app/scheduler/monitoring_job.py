from sqlmodel import Session, select

from app.config.database import engine
from app.models.dataset import Dataset
from app.models.data_source import DataSource

from app.services.monitoring_service import (
    MonitoringService,
)
from app.services.snapshot_service import (
    SnapshotService,
)


def run_monitoring():

    print("InsightFlow monitoring job started")

    monitoring_service = MonitoringService()
    snapshot_service = SnapshotService()

    with Session(engine) as session:

        datasets = session.exec(
            select(Dataset)
            .where(
                Dataset.monitoring_enabled.is_(True)
            )
        ).all()

        for dataset in datasets:

            try:

                data_source = session.exec(
                    select(DataSource)
                    .where(
                        DataSource.dataset_id == dataset.id
                    )
                ).first()

                if not data_source:

                    print(
                        f"Dataset {dataset.id}: "
                        "No data source configured"
                    )

                    continue

                snapshot = (
                    snapshot_service
                    .create_snapshot_from_database(
                        session=session,
                        dataset_id=dataset.id,
                        data_source=data_source,
                    )
                )

                if not snapshot:

                    print(
                        f"Dataset {dataset.id}: "
                        "No data change detected"
                    )

                    continue

                print(
                    f"Dataset {dataset.id}: "
                    f"New snapshot v{snapshot.version}"
                )

                result = (
                    monitoring_service.monitor_dataset(
                        session=session,
                        dataset_id=dataset.id,
                    )
                )

                dataset.last_processed_snapshot_id = (
                    snapshot.id
                )

                session.add(dataset)
                session.commit()

                if result["threshold"].triggered:

                    print(
                        f"ALERT detected for "
                        f"dataset {dataset.id}"
                    )

                else:

                    print(
                        f"No significant change "
                        f"for dataset {dataset.id}"
                    )

            except Exception as exc:

                session.rollback()

                print(
                    f"Monitoring failed for "
                    f"dataset {dataset.id}: {exc}"
                )

    print(
        "InsightFlow monitoring job finished"
    )