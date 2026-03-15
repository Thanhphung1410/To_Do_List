from sqlmodel import SQLModel, create_engine

from app.core.config import settings

engine = create_engine(settings.database_url, echo=settings.debug)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
