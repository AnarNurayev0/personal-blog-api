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

class AdminMe(SQLModel):
    id: int
    username: str
    role: str
    created_at: datetime