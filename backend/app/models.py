from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)


class Cargo(Base):
    __tablename__ = "cargo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cargo_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    origin: Mapped[str] = mapped_column(String, nullable=False)
    destination: Mapped[str] = mapped_column(String, nullable=False)
    weight_kg: Mapped[int] = mapped_column(Integer, nullable=False)
    manifest_date: Mapped[str] = mapped_column(String, nullable=True)
