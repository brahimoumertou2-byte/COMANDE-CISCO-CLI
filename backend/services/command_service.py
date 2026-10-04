import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "commands.json"


def load_command_dataset() -> list[dict]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def seed_commands(db: Session) -> int:
    existing = db.scalar(select(models.Command.id).limit(1))
    if existing is not None:
        return 0

    rows = [models.Command(**item) for item in load_command_dataset()]
    db.add_all(rows)
    db.commit()
    return len(rows)
