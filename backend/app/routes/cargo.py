from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..db import get_db
from ..models import Cargo, User
from ..parser import apply_business_rules, parse_manifest
from ..rbac import require_role
from ..schemas import CargoOut, UploadResultOut

router = APIRouter(prefix="/api", tags=["cargo"])


@router.get("/cargo", response_model=list[CargoOut])
def list_cargo(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Cargo]:
    return db.query(Cargo).order_by(Cargo.id).all()


@router.post("/upload", response_model=UploadResultOut)
async def upload_manifest(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: User = Depends(require_role("Admin")),
) -> UploadResultOut:
    content = (await file.read()).decode("utf-8", errors="replace")
    stats = parse_manifest(content)
    saveable, skipped_prime = apply_business_rules(stats.rows)
    for row in saveable:
        db.add(
            Cargo(
                cargo_id=row["cargo_id"],
                origin=row["origin"],
                destination=row["destination"],
                weight_kg=row["weight_kg"],
            )
        )
    db.commit()
    return UploadResultOut(
        received=len(stats.rows),
        saved=len(saveable),
        skipped_prime=skipped_prime,
        malformed=stats.malformed,
    )
