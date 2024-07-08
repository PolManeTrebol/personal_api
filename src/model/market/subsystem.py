from typing import Any

from sqlalchemy import Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column
from src.connection.database import Database


database: Database = Database()
Base: Any = database.db.Model


class Subsystem(Base):
    __tablename__ = 'subsystem'
    __table_args__ = (
        PrimaryKeyConstraint('idsubsystem', name='subsystem_pkey'),
        {'schema': 'market'}
    )

    idsubsystem: Mapped[int] = mapped_column(Integer, primary_key=True)
    subsystem: Mapped[str] = mapped_column(String(255), nullable=False)

