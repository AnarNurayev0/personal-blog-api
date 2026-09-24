from fastapi import APIRouter, status, Depends, HTTPException
from app.database import get_session
from sqlalchemy.orm import Session
from ..auth import require_admin
from app import schemas, models
from typing import List

router = APIRouter(prefix="/admin",tags=["admin"],dependencies=[Depends(require_admin)])

# === ADMIN URLS ===

# --- GET ME ---
@router.get("/me", status_code=status.HTTP_200_OK)
def me(admin: models.Users = Depends(require_admin)):

    return {"username": admin.username, "role": admin.role}

# --- GET ALL ARTICLES - [DETAILED] ---
@router.get("/articles",status_code=status.HTTP_200_OK,response_model=List[schemas.ArticleDetailed])
def get_all_articles(db: Session = Depends(get_session)):

    articles = db.query(models.Articles).all()

    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"articles are not found!")

    return articles

# --- GET AN ARTICLE BY ID - [DETAILED] ---
@router.get("/articles/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ArticleDetailed)
def get_article_by_id(id: int, db: Session = Depends(get_session)):

    article = db.query(models.Articles).filter(models.Articles.id == id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"article with {id} is not found")

    return article

# --- CREATE ARTICLE ---
@router.post("/articles",status_code=status.HTTP_201_CREATED)
def create_article(article: schemas.ArticleInput, db: Session = Depends(get_session)):
    pass