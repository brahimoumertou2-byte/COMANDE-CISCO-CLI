from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from . import models, schemas


def list_commands(
    db: Session,
    category: str | None = None,
    device: str | None = None,
) -> list[models.Command]:
    stmt = select(models.Command).order_by(models.Command.command.asc())
    if category:
        stmt = stmt.where(models.Command.category == category)
    if device:
        stmt = stmt.where(models.Command.device == device)
    return list(db.scalars(stmt).all())


def get_command(db: Session, command_id: int) -> models.Command | None:
    return db.get(models.Command, command_id)


def search_commands(db: Session, query: str) -> list[models.Command]:
    pattern = f"%{query.lower()}%"
    stmt = (
        select(models.Command)
        .where(
            models.Command.command.ilike(pattern)
            | models.Command.description.ilike(pattern)
            | models.Command.category.ilike(pattern)
        )
        .order_by(models.Command.command.asc())
    )
    return list(db.scalars(stmt).all())


def create_command(db: Session, payload: schemas.CommandCreate) -> models.Command:
    row = models.Command(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def delete_all_commands(db: Session) -> None:
    db.execute(delete(models.Command))
    db.commit()
