from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.alert import Alert
from app.schemas.threshold_schema import ThresholdAlert


class AlertService:

    def create_alerts(
        self,
        session: Session,
        dataset_id: int,
        snapshot_id: int,
        alerts: list[ThresholdAlert],
    ) -> list[Alert]:

        created_alerts = []

        for alert_data in alerts:

            if self.alert_exists(
                session=session,
                dataset_id=dataset_id,
                snapshot_id=snapshot_id,
                column=alert_data.column,
                metric=alert_data.metric,
            ):
                continue

            alert = Alert(
                dataset_id=dataset_id,
                snapshot_id=snapshot_id,
                metric=alert_data.metric,
                column=alert_data.column,
                old_value=alert_data.old_value,
                new_value=alert_data.new_value,
                percentage_change=(
                    alert_data.percentage_change
                ),
                threshold=alert_data.threshold,
                direction=alert_data.direction,
            )

            session.add(alert)

            created_alerts.append(alert)

        session.commit()

        for alert in created_alerts:
            session.refresh(alert)

        return created_alerts


    def get_dataset_alerts(
        self,
        session: Session,
        dataset_id: int
    ) -> list[Alert]:

        return session.exec(
            select(Alert)
            .where(
                Alert.dataset_id == dataset_id
            )
            .order_by(
                Alert.created_at.desc()
            )
        ).all()


    def get_active_alerts(
    self,
    session: Session,
    dataset_id: int
) -> list[Alert]:

        statement = (
            select(Alert)
            .where(
                Alert.dataset_id == dataset_id
            )
            .where(
                Alert.status == "active"
            )
            .order_by(
                Alert.created_at.desc()
            )
        )

        return session.exec(statement).all()


    def resolve_alert(
        self,
        session: Session,
        alert_id: int
    ) -> Alert:

        alert = session.get(
            Alert,
            alert_id
        )

        if not alert:
            raise HTTPException(
                status_code=404,
                detail="Alert not found"
            )

        alert.status = "resolved"

        session.add(alert)
        session.commit()
        session.refresh(alert)

        return alert


    def alert_exists(
        self,
        session: Session,
        dataset_id: int,
        snapshot_id: int,
        column: str | None,
        metric: str,
    ) -> bool:

        alert = session.exec(
            select(Alert)
            .where(
                Alert.dataset_id == dataset_id,
                Alert.snapshot_id == snapshot_id,
                Alert.column == column,
                Alert.metric == metric,
            )
        ).first()

        return alert is not None