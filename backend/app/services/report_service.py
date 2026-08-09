import json

from fastapi import HTTPException
from sqlalchemy import func
from sqlmodel import Session, select

from app.models.alert import Alert
from app.models.dataset import Dataset
from app.models.report import Report
from app.models.snapshot import Snapshot


class ReportService:

    def generate_report(
        self,
        session: Session,
        dataset_id: int,
        report_type: str = "monitoring",
    ) -> Report:

        dataset = session.get(
            Dataset,
            dataset_id,
        )

        if not dataset:

            raise HTTPException(
                status_code=404,
                detail="Dataset not found",
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
                Alert.status == "active",
            )
        ).one()

        resolved_alerts = session.exec(
            select(func.count())
            .select_from(Alert)
            .where(
                Alert.dataset_id == dataset_id,
                Alert.status == "resolved",
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

            latest_snapshot_data = {
                "id": latest_snapshot.id,
                "version": latest_snapshot.version,
                "rows": latest_snapshot.rows,
                "columns": latest_snapshot.columns,
                "created_at": (
                    latest_snapshot.created_at.isoformat()
                ),
            }

        report_content = {
            "dataset": {
                "id": dataset.id,
                "name": dataset.name,
                "monitoring_enabled": (
                    dataset.monitoring_enabled
                ),
            },
            "monitoring": {
                "total_snapshots": total_snapshots,
                "active_alerts": active_alerts,
                "resolved_alerts": resolved_alerts,
                "last_processed_snapshot_id": (
                    dataset.last_processed_snapshot_id
                ),
            },
            "latest_snapshot": latest_snapshot_data,
        }

        report = Report(
            dataset_id=dataset_id,
            report_type=report_type,
            content=json.dumps(
                report_content,
                indent=2,
            ),
        )

        session.add(report)
        session.commit()
        session.refresh(report)

        return report


    def get_dataset_reports(
        self,
        session: Session,
        dataset_id: int,
    ) -> list[Report]:

        return session.exec(
            select(Report)
            .where(
                Report.dataset_id == dataset_id
            )
            .order_by(
                Report.created_at.desc()
            )
        ).all()


    def get_report(
        self,
        session: Session,
        report_id: int,
    ) -> Report:

        report = session.get(
            Report,
            report_id,
        )

        if not report:

            raise HTTPException(
                status_code=404,
                detail="Report not found",
            )

        return report