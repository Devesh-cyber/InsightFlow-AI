from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Dataset(SQLModel, table=True):
    
    __tablename__ = 'datasets'
    id: Optional[int] = Field(None, primary_key=True)
    name: str = Field(index=True)
    filename: str
    file_path: str
    extension: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now)