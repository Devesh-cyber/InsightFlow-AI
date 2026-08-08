from sqlmodel import SQLModel

class ThresholdRule(SQLModel):
    threshold_percentage: float = 10.0


class ThresholdAlert(SQLModel):

    metric: str
    column: str | None = None
    old_value: float
    new_value: float
    percentage_change: float
    threshold: float
    direction: str


class ThresholdResult(SQLModel):

    triggered: bool
    alerts: list[ThresholdAlert] = []
