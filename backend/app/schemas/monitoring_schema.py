from datetime import datetime
from pydantic import BaseModel
from typing import Literal

class LatestSnapshotSummary(BaseModel):
    id: int
    version: int
    created_at: datetime


class MonitoringSummary(BaseModel):
    dataset_id: int
    monitoring_enabled: bool

    total_snapshots: int
    last_processed_snapshot_id: int | None

    active_alerts: int
    resolved_alerts: int

    latest_snapshot: LatestSnapshotSummary | None


class SnapshotHistoryResponse(BaseModel):
    id: int
    version: int
    rows: int
    columns: int
    dataset_hash: str
    created_at: datetime

class TimelineEvent(BaseModel):
    type: Literal["snapshot", "alert"]

    id: int
    snapshot_id: int | None = None
    version: int | None = None

    column: str | None = None
    metric: str | None = None
    percentage_change: float | None = None
    status: str | None = None

    created_at: datetime