from sqlmodel import SQLModel
from datetime import datetime

class ArticleBase(SQLModel):
    id: int
    title: str
    published: bool

class ArticleOut(ArticleBase):
    content: str
    created_at: datetime

class ArticleDetailed(ArticleOut):
    author_id: int
    updated_at: datetime

class ArticleInput(SQLModel):
    title: str
    content: str
    published: bool = True

class ArticleInputPut(SQLModel):
    title: str
    content: str
    published: bool = True

class ArticleInputPatch(SQLModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None

class Users(SQLModel):
    id: int
    username: str
    role: str
    created_at: datetime

class AdminCreate(SQLModel):
    username: str
    password: str
