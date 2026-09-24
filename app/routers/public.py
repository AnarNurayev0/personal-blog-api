from fastapi import APIRouter, status, Depends, HTTPException
from app.database import get_session
from sqlalchemy.orm import Session
from app import schemas, models
from typing import List

router = APIRouter(prefix="/articles",tags=["public"])


# === PUBLIC URLS ===

# --- GET ALL ARTICLES ---
@router.get("",status_code=status.HTTP_200_OK,response_model=List[schemas.ArticleBase])
def get_all_articles(db: Session = Depends(get_session)):

    articles = db.query(models.Articles).all()

    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"articles are not found!")

    return articles

# --- GET AN ARTICLE BY ID ---
@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ArticleOut)
def get_article_by_id(id: int, db: Session = Depends(get_session)):

    article = db.query(models.Articles).filter(models.Articles.id == id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"article with {id} is not found")

    return article

