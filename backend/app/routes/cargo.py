from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..db import get_db
from ..models import Cargo, User
from ..schemas import CargoOut

router = APIRouter(prefix="/api", tags=["cargo"])


@router.get("/cargo", response_model=list[CargoOut])
def list_cargo(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Cargo]:
    return db.query(Cargo).order_by(Cargo.id).all()
