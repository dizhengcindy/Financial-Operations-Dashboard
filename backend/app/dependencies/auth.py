from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.security import decode_token_subject

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise credentials_exception
    sub = decode_token_subject(credentials.credentials)
    if sub is None:
        raise credentials_exception
    try:
        user_id = UUID(sub)
    except ValueError:
        raise credentials_exception
    user = (
        db.query(User)
        .filter(User.id == user_id, User.deleted.is_(False))
        .first()
    )
    if user is None:
        raise credentials_exception
    return user


def get_current_user_id(user: User = Depends(get_current_user)) -> UUID:
    return user.id
