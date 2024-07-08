from typing import Any

from sqlalchemy import Integer, Float, String, TIMESTAMP, PrimaryKeyConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from src.connection.database import Database


database: Database = Database()
Base: Any = database.db.Model


class IdealRetailerCurveH(Base):
    __tablename__ = 'ideal_retailer_curve_h'
    __table_args__ = (
        PrimaryKeyConstraint('datetime', 'cups', 'tariff', 'subsystem', 'idprovince',
                             name='ideal_retailer_curve_h_pk'),
        Index('ideal_retailer_curve_h_datetime_idx', 'datetime',
              postgresql_using='btree'),
        Index('ideal_retailer_curve_h_idprovince_datetime_idx', 'idprovince', 'datetime',
              postgresql_using='btree'),
        {'schema': 'data'}
    )

    datetime: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False)
    cups: Mapped[str] = mapped_column(String, nullable=False)
    activein: Mapped[float] = mapped_column(Float)
    activeout: Mapped[float] = mapped_column(Float)
    tariff: Mapped[str] = mapped_column(String, nullable=False)
    subsystem: Mapped[str] = mapped_column(String, nullable=False)
    supply_address_cp: Mapped[str] = mapped_column(String)
    idmunicipality: Mapped[int] = mapped_column(Integer)
    idprovince: Mapped[int] = mapped_column(Integer, nullable=False)
    idretailer_int: Mapped[int] = mapped_column(Integer)
