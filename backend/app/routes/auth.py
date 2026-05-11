from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import hash_password
from ..db import get_db
from ..models import User
from ..schemas import SignupIn, UserOut

router = APIRouter(tags=["auth"])

ADMIN_EMAIL_DOMAIN = "@nebula-corp.com"


def assign_role(email: str) -> str:
    return "Admin" if email.lower().endswith(ADMIN_EMAIL_DOMAIN) else "Standard"


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupIn, db: Session = Depends(get_db)) -> User:
    email = payload.email.lower()
    if db.query(User).filter(User.email == email).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered.",
        )

    user = User(
        email=email,
        password_hash=hash_password(payload.password),
        role=assign_role(email),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
