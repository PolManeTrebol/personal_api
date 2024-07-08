from typing import Any

from sqlalchemy import Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column
from src.connection.database import Database


database: Database = Database()
Base: Any = database.db.Model


class Tariff(Base):
    __tablename__ = 'tariff'
    __table_args__ = (
        PrimaryKeyConstraint('idtariff', name='tariff_pkey'),
        {'schema': 'market'}
    )

    idtariff: Mapped[int] = mapped_column(Integer, primary_key=True)
    tariff: Mapped[str] = mapped_column(String(255), nullable=False)
