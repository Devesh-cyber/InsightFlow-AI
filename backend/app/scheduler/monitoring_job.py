from sqlmodel import Session, select

from app.config.database import engine
from app.models.dataset import Dataset
from app.models.snapshot import Snapshot
from app.services.monitoring_service import MonitoringService

def run_monitoring():

    print('Indighflow monitoring job started')

    monitoring_service = MonitoringService()

    with Session(engine) as session:

        datasets = session.exec(
            select(Dataset)
            .where(
                Dataset.monitoring_enabled.is_(True)
            )
        ).all()

        for dataset in datasets:

            try:

                latest_snapshot = session.exec(
                    select(Snapshot)
                    .where(
                        Snapshot.dataset_id == dataset.id
                    )
                    .order_by(
                        Snapshot.version.desc()
                    )
                ).first()

                if latest_snapshot is None:
                    print(
                        f"No snapshots for dataset "
                        f"{dataset.id}"
                    )
                    continue

                if (
                    dataset.last_processed_snapshot_id
                    == latest_snapshot.id
                ):
                    print(
                        f"Dataset {dataset.id}: "
                        f"No new snapshot. Skipping."
                    )
                    continue

                print(
                    f"Monitoring dataset: "
                    f"{dataset.id}"
                )

                result = (
                    monitoring_service.monitor_dataset(
                        session=session,
                        dataset_id=dataset.id,
                    )
                )

                dataset.last_processed_snapshot_id = (
                    latest_snapshot.id
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

                print(
                    f"Monitoring failed for "
                    f"dataset {dataset.id}: {exc}"
                )
    print("InsightFlow monitoring job finished")