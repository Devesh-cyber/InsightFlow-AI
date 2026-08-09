from datetime import datetime

from pydantic import BaseModel


class LatestSnapshotResponse(BaseModel):
    id: int
    version: int
    rows: int
    columns: int
    created_at: datetime


class MonitoringSummaryResponse(BaseModel):
    dataset_id: int
    dataset_name: str

    total_snapshots: int

    latest_snapshot: (
        LatestSnapshotResponse | None
    )

    active_alerts: int
    resolved_alerts: int

    last_processed_snapshot_id: int | None