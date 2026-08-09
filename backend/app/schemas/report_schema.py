from datetime import datetime

from pydantic import BaseModel


class ReportCreate(BaseModel):

    report_type: str = "monitoring"


class ReportResponse(BaseModel):

    id: int

    dataset_id: int

    report_type: str

    content: str

    created_at: datetime