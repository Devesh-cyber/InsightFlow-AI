import pandas as pd

from fastapi import HTTPException
from sqlalchemy import func
from sqlmodel import Session, select

from app.engines.comparison_engine import ComparisonEngine
from app.engines.threshold_engine import ThresholdEngine

from app.models.alert import Alert
from app.models.dataset import Dataset
from app.models.snapshot import Snapshot

from app.schemas.monitoring_schema import (
    LatestSnapshotSummary,
    MonitoringSummary,
    TimelineEvent,
)
from app.schemas.threshold_schema import ThresholdRule

from app.services.alert_service import AlertService
from app.services.threshold_service import ThresholdService


class MonitoringService:

    def __init__(self):

        self.comparison_engine = ComparisonEngine()

        self.threshold_engine = ThresholdEngine()

        self.threshold_service = ThresholdService()

        self.alert_service = AlertService()


    def monitor_dataset(
        self,
        session: Session,
        dataset_id: int,
    ):

        snapshots = session.exec(
            select(Snapshot)
            .where(
                Snapshot.dataset_id == dataset_id
            )
            .order_by(
                Snapshot.version.desc()
            )
        ).all()

        if len(snapshots) < 2:

            raise HTTPException(
                status_code=400,
                detail=(
                    "At least two snapshots "
                    "are required for comparison"
                ),
            )

        latest_snapshot = snapshots[0]

        previous_snapshot = snapshots[1]

        old_df = self._load_snapshot(
            previous_snapshot
        )

        new_df = self._load_snapshot(
            latest_snapshot
        )

        report = self.comparison_engine.compare(
            old_snapshot_id=previous_snapshot.id,
            new_snapshot_id=latest_snapshot.id,
            old_df=old_df,
            new_df=new_df,
        )

        threshold_config = (
            self.threshold_service.get_threshold(
                session=session,
                dataset_id=dataset_id,
            )
        )

        threshold_result = (
            self.threshold_engine.evaluate(
                report=report,
                rule=ThresholdRule(
                    threshold_percentage=(
                        threshold_config
                        .threshold_percentage
                    )
                ),
            )
        )

        created_alerts = []

        if threshold_result.triggered:

            created_alerts = (
                self.alert_service.create_alerts(
                    session=session,
                    dataset_id=dataset_id,
                    snapshot_id=latest_snapshot.id,
                    alerts=threshold_result.alerts,
                )
            )

        return {
            "comparison": report,
            "threshold": threshold_result,
            "alerts": created_alerts,
        }


    def _load_snapshot(
        self,
        snapshot: Snapshot,
    ) -> pd.DataFrame:

        return pd.read_parquet(
            snapshot.parquet_path
        )


    def get_monitoring_summary(
        self,
        session: Session,
        dataset_id: int,
    ) -> MonitoringSummary:

        dataset = session.get(
            Dataset,
            dataset_id
        )

        if not dataset:

            raise HTTPException(
                status_code=404,
                detail="Dataset not found"
            )

        total_snapshots = session.exec(
            select(func.count())
            .select_from(Snapshot)
            .where(
                Snapshot.dataset_id == dataset_id
            )
        ).one()

        active_alerts = session.exec(
            select(func.count())
            .select_from(Alert)
            .where(
                Alert.dataset_id == dataset_id,
                Alert.status == "active"
            )
        ).one()

        resolved_alerts = session.exec(
            select(func.count())
            .select_from(Alert)
            .where(
                Alert.dataset_id == dataset_id,
                Alert.status == "resolved"
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

        latest_snapshot_data = None

        if latest_snapshot:

            latest_snapshot_data = (
                LatestSnapshotSummary(
                    id=latest_snapshot.id,
                    version=latest_snapshot.version,
                    created_at=latest_snapshot.created_at,
                )
            )

        return MonitoringSummary(
            dataset_id=dataset.id,
            monitoring_enabled=dataset.monitoring_enabled,

            total_snapshots=total_snapshots,

            last_processed_snapshot_id=(
                dataset.last_processed_snapshot_id
            ),

            active_alerts=active_alerts,
            resolved_alerts=resolved_alerts,

            latest_snapshot=latest_snapshot_data,
        )


    def get_snapshot_history(
        self,
        session: Session,
        dataset_id: int,
    ) -> list[Snapshot]:

        dataset = session.get(
            Dataset,
            dataset_id
        )

        if not dataset:

            raise HTTPException(
                status_code=404,
                detail="Dataset not found"
            )

        return session.exec(
            select(Snapshot)
            .where(
                Snapshot.dataset_id == dataset_id
            )
            .order_by(
                Snapshot.version.desc()
            )
        ).all()


    def get_monitoring_timeline(
        self,
        session: Session,
        dataset_id: int,
    ) -> list[TimelineEvent]:

        dataset = session.get(
            Dataset,
            dataset_id
        )

        if not dataset:

            raise HTTPException(
                status_code=404,
                detail="Dataset not found"
            )

        snapshots = session.exec(
            select(Snapshot)
            .where(
                Snapshot.dataset_id == dataset_id
            )
        ).all()

        alerts = session.exec(
            select(Alert)
            .where(
                Alert.dataset_id == dataset_id
            )
        ).all()

        timeline = []

        for snapshot in snapshots:

            timeline.append(
                TimelineEvent(
                    type="snapshot",
                    id=snapshot.id,
                    snapshot_id=snapshot.id,
                    version=snapshot.version,
                    created_at=snapshot.created_at,
                )
            )

        for alert in alerts:

            timeline.append(
                TimelineEvent(
                    type="alert",
                    id=alert.id,
                    snapshot_id=alert.snapshot_id,
                    column=alert.column,
                    metric=alert.metric,
                    percentage_change=(
                        alert.percentage_change
                    ),
                    status=alert.status,
                    created_at=alert.created_at,
                )
            )

        timeline.sort(
            key=lambda event: event.created_at,
            reverse=True,
        )

        return timeline