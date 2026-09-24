from argon2.exceptions import InvalidHashError, VerificationError
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from argon2 import PasswordHasher
from .database import get_session
from .models import Users

security = HTTPBasic()
ph = PasswordHasher()
DUMMY_HASH = ph.hash("dummy-parol")


def check_pass(stored_hash: str, plain: str) -> bool:
    
    try:

        return ph.verify(stored_hash, plain)
    
    except (VerificationError, InvalidHashError):
        
        return False


def get_current_user(creds: HTTPBasicCredentials = Depends(security),session: Session = Depends(get_session),) -> Users:
    
    user = session.exec(select(Users).where(Users.username == creds.username)).first()

    hash_to_check = user.password if user else DUMMY_HASH
    ok = check_pass(hash_to_check, creds.password)

    if not user or not ok:
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid credentials!", 
                            headers={"WWW-Authenticate": "Basic"})
    
    return user


def require_admin(user: Users = Depends(get_current_user)) -> Users:
    
    if user.role != "admin":

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden!")
    
    return user