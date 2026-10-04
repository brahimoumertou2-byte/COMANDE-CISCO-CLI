from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("", response_model=list[schemas.CommandRead])
def search(q: str = Query(min_length=1), db: Session = Depends(get_db)):
    return crud.search_commands(db, q)
