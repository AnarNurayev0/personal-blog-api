from fastapi import APIRouter, status, Depends, HTTPException, Request
from app.database import get_session
from sqlalchemy.orm import Session
from app import schemas, models
from ..limiter import limiter
from typing import List

router = APIRouter(prefix="/articles",tags=["Public Articles"])


# === PUBLIC URLS ===

# --- GET ALL ARTICLES ---
@router.get("",status_code=status.HTTP_200_OK,response_model=List[schemas.ArticleBase])
@limiter.limit("30/minute")
def get_all_articles(request: Request , db: Session = Depends(get_session)):

    articles = db.query(models.Articles).filter(models.Articles.published == True).all()

    return articles

# --- GET AN ARTICLE BY ID ---
@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ArticleOut)
@limiter.limit("60/minute")
def get_article_by_id(request: Request, id: int, db: Session = Depends(get_session)):

    article = db.query(models.Articles).filter(models.Articles.id == id, models.Articles.published == True).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"article with id:{id} is not found")

    return article
