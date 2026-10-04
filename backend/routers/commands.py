from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/commands", tags=["commands"])


@router.get("", response_model=list[schemas.CommandRead])
def list_commands(
    category: str | None = Query(default=None),
    device: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return crud.list_commands(db, category=category, device=device)


@router.get("/{command_id}", response_model=schemas.CommandRead)
def get_command(command_id: int, db: Session = Depends(get_db)):
    row = crud.get_command(db, command_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Command not found")
    return row
