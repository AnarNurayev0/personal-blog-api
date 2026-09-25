from fastapi import APIRouter, status, Depends, HTTPException
from app.database import get_session
from sqlalchemy.orm import Session
from ..auth import require_admin
from app import schemas, models
from ..auth import hash_pass
from typing import List

router = APIRouter(prefix="/admin", tags=["Admin Management"], dependencies=[Depends(require_admin)])

# === ADMIN URLS ===

# --- GET ME ---
@router.get("/me", status_code=status.HTTP_200_OK,response_model=schemas.Users)
def me(admin: models.Users = Depends(require_admin)):

    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"admin is not found!")

    return admin

# --- CREATE ADMIN ---
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Users)
def create_admin(user: schemas.AdminCreate, db: Session = Depends(get_session)):

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user data is not found!")

    hashed_password = hash_pass(user.password)
    user.password = hashed_password

    db_user = models.Users(role="admin", **user.model_dump())

    # print(db_user)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
            
    return db_user


# --- GET ALL USERS ---
@router.get("/users", status_code=status.HTTP_200_OK,response_model=List[schemas.Users])
def get_all_users(db: Session = Depends(get_session)):

    users = db.query(models.Users).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"users are not found!")

    return users