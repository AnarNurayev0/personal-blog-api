from fastapi import APIRouter, status, Depends, HTTPException
from app import schemas, models, auth
from app.database import get_session
from sqlalchemy.orm import Session
from ..auth import require_admin
from typing import List

router = APIRouter(prefix="/admin",tags=["admin"],dependencies=[Depends(require_admin)])

# === ADMIN URLS ===

# --- GET ME ---
@router.get("/me", status_code=status.HTTP_200_OK,response_model=schemas.AdminMe)
def me(admin: models.Users = Depends(require_admin)):

    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"admin is not found!")

    return admin

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

# --- CREATE AN ARTICLE ---
@router.post("/articles",status_code=status.HTTP_201_CREATED,response_model=schemas.ArticleDetailed)
def create_article(article: schemas.ArticleInput, db: Session = Depends(get_session), admin: models.Users = Depends(require_admin)):

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the article is not found!")

    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    article = models.Articles(author_id = admin.id, **article.dict())
    # print(article.dict())

    db.add(article)
    db.commit()
    db.refresh(article)

    # print(article.dict())
    
    return article

# --- UPDATE AN ARTICLE ---
@router.put("/articles/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ArticleDetailed)
def update_article(article: schemas.ArticleInput, id: int, db: Session = Depends(get_session)):

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

# --- DELETE AN ARTICLE ---
@router.delete("/articles/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_article_by_id(id: int, db: Session = Depends(get_session)):

    if not id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"id is not found!")

    article = db.query(models.Articles).filter(models.Articles.id == id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"article is not found!")

    db.delete(article)
    db.commit()

    return