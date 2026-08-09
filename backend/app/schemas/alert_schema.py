from datetime import datetime
from pydantic import BaseModel


class AlertResponse(BaseModel):
    id: int

    dataset_id: int
    snapshot_id: int

    metric: str
    column: str | None

    old_value: float | None
    new_value: float | None

    percentage_change: float
    threshold: float
    direction: str

    status: str

    created_at: datetime