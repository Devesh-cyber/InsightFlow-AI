from sqlmodel import SQLModel, Session, create_engine

from app.config.settings import settings
from app.models.alert import Alert

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session