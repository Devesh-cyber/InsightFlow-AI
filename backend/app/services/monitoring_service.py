import pandas as pd

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.snapshot import Snapshot
from app.engines.comparison_engine import ComparisonEngine
from app.engines.threshold_engine import ThresholdEngine
from app.schemas.threshold_schema import ThresholdRule
from app.services.threshold_service import ThresholdService
from app.services.alert_service import AlertService

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

        # --------------------------------
        # 1. Get snapshots for dataset
        # --------------------------------

        snapshots = session.exec(
            select(Snapshot)
            .where(
                Snapshot.dataset_id == dataset_id
            )
            .order_by(
                Snapshot.version.desc()
            )
        ).all()

        # --------------------------------
        # 2. Need at least 2 snapshots
        # --------------------------------

        if len(snapshots) < 2:

            raise HTTPException(
                status_code=400,
                detail=(
                    "At least two snapshots "
                    "are required for comparison"
                ),
            )

        # --------------------------------
        # 3. Select latest two snapshots
        # --------------------------------

        latest_snapshot = snapshots[0]

        previous_snapshot = snapshots[1]

        # --------------------------------
        # 4. Load Parquet files
        # --------------------------------

        old_df = self._load_snapshot(
            previous_snapshot
        )

        new_df = self._load_snapshot(
            latest_snapshot
        )

        # --------------------------------
        # 5. Compare snapshots
        # --------------------------------

        report = self.comparison_engine.compare(
            old_snapshot_id=previous_snapshot.id,
            new_snapshot_id=latest_snapshot.id,
            old_df=old_df,
            new_df=new_df,
        )

        # --------------------------------
        # 6. Get dataset threshold
        # --------------------------------

        threshold_config = (
            self.threshold_service.get_threshold(
                session=session,
                dataset_id=dataset_id,
            )
        )

        # --------------------------------
        # 7. Evaluate threshold
        # --------------------------------

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
        # --------------------------------
        # 8. Return both results
        # --------------------------------

        return {
            "comparison": report,
            "threshold": threshold_result,
            'alerts': created_alerts
        }

    def _load_snapshot(
        self,
        snapshot: Snapshot,
    ) -> pd.DataFrame:

        return pd.read_parquet(
            snapshot.parquet_path
        )