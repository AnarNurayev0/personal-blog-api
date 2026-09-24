from sqlmodel import Field, SQLModel, TIMESTAMP, text, func
from datetime import datetime

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    role: str = Field(nullable=False, sa_column_kwargs={"server_default": text("'user'")})
    created_at: datetime = Field(sa_type=TIMESTAMP(timezone=True),
                                nullable=False,
                                sa_column_kwargs={"server_default": text("now()")})

class Articles(SQLModel, table=True):
    id: int | None = Field(primary_key=True, nullable=False, default=None)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(nullable=False, sa_column_kwargs={"server_default": text("True")})
    author_id: int = Field(nullable=False, foreign_key='users.id')
    created_at: datetime = Field(sa_type=TIMESTAMP(timezone=True),
                                nullable=False,
                                sa_column_kwargs={"server_default": text("now()")})
    updated_at: datetime = Field(sa_type=TIMESTAMP(timezone=True),
                                nullable=False,
                                sa_column_kwargs={"server_default": text("now()"), "onupdate": func.now()})