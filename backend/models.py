from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Command(Base):
    __tablename__ = "commands"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    command: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    device: Mapped[str] = mapped_column(String(50), default="Router")
    mode: Mapped[str] = mapped_column(String(80), default="Privileged EXEC")
    description: Mapped[str] = mapped_column(Text)
    syntax: Mapped[str] = mapped_column(Text)
    example: Mapped[str] = mapped_column(Text)
    platform: Mapped[str] = mapped_column(String(100), default="Cisco IOS / IOS XE")
