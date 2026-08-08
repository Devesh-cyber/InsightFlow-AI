from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.threshold import DatasetThreshold


class ThresholdService:

    def get_threshold(
            self,
            session: Session,
            dataset_id: str
    ) -> DatasetThreshold:

        threshold = session.exec(
            select(DatasetThreshold)
            .where(
                DatasetThreshold.dataset_id == dataset_id
            )
        ).first()

        if threshold is None:

            threshold = DatasetThreshold(
                dataset_id=dataset_id,
                threshold_percentage=10.0,
            )

            session.add(threshold)
            session.commit()
            session.refresh(threshold)

        return threshold

    def set_threshold(
        self,
        session: Session,
        dataset_id: int,
        threshold_percentage: float,
    ) -> DatasetThreshold:

        if threshold_percentage < 0:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Threshold percentage "
                    "cannot be negative."
                ),
            )

        threshold = session.exec(
            select(DatasetThreshold)
            .where(
                DatasetThreshold.dataset_id
                == dataset_id
            )
        ).first()

        if threshold is None:

            threshold = DatasetThreshold(
                dataset_id=dataset_id,
                threshold_percentage=(
                    threshold_percentage
                ),
            )

        else:

            threshold.threshold_percentage = (
                threshold_percentage
            )

        session.add(threshold)
        session.commit()
        session.refresh(threshold)

        return threshold