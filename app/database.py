from sqlmodel import Session, create_engine
from .settings import settings
from typing import Annotated
from fastapi import Depends

DATABASE_URL = settings.database_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=False)


def get_session():
    with Session(engine) as session:
        yield session

# === DATABASE DEPENDENCY ===
DatabaseDep = Annotated[Session, Depends(get_session)]