from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..db import get_db
from ..models import Cargo, User
from ..rbac import require_role
from ..schemas import CargoOut, UploadResultOut

router = APIRouter(prefix="/api", tags=["cargo"])


def _parse_pipe_delimited(text: str) -> tuple[list[dict], int]:
    rows: list[dict] = []
    malformed = 0
    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if line_no == 1 and "WEIGHT" in line.upper():
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 4:
            malformed += 1
            continue
        try:
            weight = float(parts[3])
        except ValueError:
            malformed += 1
            continue
        rows.append(
            {
                "cargo_id": parts[0],
                "origin": parts[1],
                "destination": parts[2],
                "weight": weight,
            }
        )
    return rows, malformed


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
    rows, malformed = _parse_pipe_delimited(content)
    for row in rows:
        db.add(
            Cargo(
                cargo_id=row["cargo_id"],
                origin=row["origin"],
                destination=row["destination"],
                weight_kg=round(row["weight"]),
            )
        )
    db.commit()
    return UploadResultOut(
        received=len(rows),
        saved=len(rows),
        skipped_prime=0,
        malformed=malformed,
    )
