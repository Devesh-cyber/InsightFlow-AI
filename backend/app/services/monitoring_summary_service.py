from sqlmodel import Session, select, func

from app.models.dataset import Dataset
from app.models.snapshot import Snapshot
from app.models.alert import Alert


class MonitoringSummaryService:

    def get_summary(
        self,
        session: Session,
        dataset_id: int,
    ):

        dataset = session.get(
            Dataset,
            dataset_id
        )

        if not dataset:
            return None

        total_snapshots = session.exec(
            select(
                func.count(Snapshot.id)
            ).where(
                Snapshot.dataset_id == dataset_id
            )
        ).one()

        latest_snapshot = session.exec(
            select(Snapshot)
            .where(
                Snapshot.dataset_id == dataset_id
            )
            .order_by(
                Snapshot.version.desc()
            )
        ).first()

        active_alerts = session.exec(
            select(
                func.count(Alert.id)
            ).where(
                Alert.dataset_id == dataset_id,
                Alert.status == "active",
            )
        ).one()

        resolved_alerts = session.exec(
            select(
                func.count(Alert.id)
            ).where(
                Alert.dataset_id == dataset_id,
                Alert.status == "resolved",
            )
        ).one()

        return {
            "dataset_id": dataset.id,
            "dataset_name": dataset.name,
            "total_snapshots": total_snapshots,
            "latest_snapshot": latest_snapshot,
            "active_alerts": active_alerts,
            "resolved_alerts": resolved_alerts,
            "last_processed_snapshot_id": (
                dataset.last_processed_snapshot_id
            ),
        }