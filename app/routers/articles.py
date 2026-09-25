from fastapi import APIRouter, status, Depends, HTTPException
from app.database import get_session
from sqlalchemy.orm import Session
from ..auth import require_admin
from app import schemas, models
from typing import List, Union

router = APIRouter(prefix="/admin/articles", tags=["Admin Articles"], dependencies=[Depends(require_admin)])

# === ARTICLE URLS - (ONLY FOR ADMINS) ===

# --- GET ALL ARTICLES - [DETAILED] ---
@router.get("",status_code=status.HTTP_200_OK,response_model=List[schemas.ArticleDetailed])
def get_all_articles(db: Session = Depends(get_session)):

    articles = db.query(models.Articles).all()

    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"articles are not found!")

    return articles

# --- GET AN ARTICLE BY ID - [DETAILED] ---
@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ArticleDetailed)
def get_article_by_id(id: int, db: Session = Depends(get_session)):

    article = db.query(models.Articles).filter(models.Articles.id == id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"article with {id} is not found")

    return article

# --- CREATE AN ARTICLE ---
@router.post("",status_code=status.HTTP_201_CREATED,response_model=Union[schemas.ArticleDetailed, List[schemas.ArticleDetailed]])
def create_article(payload: Union[schemas.ArticleInput, List[schemas.ArticleInput]], db: Session = Depends(get_session), admin: models.Users = Depends(require_admin)):

    if isinstance(payload, list):
        if not payload:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the list is empty!")
        
        new_articles = [
            models.Articles(author_id=admin.id, **item.model_dump()) 
            for item in payload
        ]
        
        db.add_all(new_articles)
        db.commit()
        
        for article in new_articles:
            db.refresh(article)
            
        return new_articles

    else:
        new_article = models.Articles(author_id=admin.id, **payload.model_dump())
        
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        
        return new_article

# --- UPDATE AN ARTICLE - [PUT] ---
@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ArticleDetailed)
def put_article(article: schemas.ArticleInput, id: int, db: Session = Depends(get_session)):

    db_article = db.query(models.Articles).filter(id == models.Articles.id).first()

    if not (article or db_article):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the article is not found!")

    if not id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    article_data = article.model_dump(exclude_unset=True)

    db_article.sqlmodel_update(article_data)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    return db_article

# --- UPDATE AN ARTICLE - [PATCH] ---
@router.patch("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ArticleDetailed)
def patch_article(article: schemas.ArticleInputPatch, id: int, db: Session = Depends(get_session)):

    db_article = db.query(models.Articles).filter(models.Articles.id == id).first()

    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"article with id:{id} not found")

    article_data = article.model_dump(exclude_unset=True)

    db_article.sqlmodel_update(article_data)
    
    db.commit()
    db.refresh(db_article)

    return db_article

# --- DELETE AN ARTICLE ---
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_article_by_id(id: int, db: Session = Depends(get_session)):

    if not id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"id is not found!")

    article = db.query(models.Articles).filter(models.Articles.id == id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"article is not found!")

    db.delete(article)
    db.commit()

    return
