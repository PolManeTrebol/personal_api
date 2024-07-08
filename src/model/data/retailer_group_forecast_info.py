from typing import Any

from sqlalchemy import Date, Integer, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.connection.database import Database


database: Database = Database()
Base: Any = database.db.Model


class RetailerGroupForecastInfo(Base):
    __tablename__ = 'retailer_group_forecast_info'
    __table_args__ = (
        PrimaryKeyConstraint('date', 'idretailer_int', 'idsubsystem', 'idtariff', 'idgroup',
                             name='retailer_group_forecast_info_pk'), {'schema': 'data'}
    )

    date: Mapped[Date] = mapped_column(Date, nullable=False)
    idretailer_int: Mapped[int] = mapped_column(Integer, nullable=False)
    idgroup: Mapped[int] = mapped_column(Integer, nullable=False)
    idsubsystem: Mapped[int] = mapped_column(Integer, ForeignKey('market.subsystem.idsubsystem'), nullable=False)
    idtariff: Mapped[int] = mapped_column(Integer, ForeignKey('market.tariff.idtariff'), nullable=False)
    yearly_consumption: Mapped[float] = mapped_column(Float)
    cups_count: Mapped[int] = mapped_column(Integer)
    validation: Mapped[int] = mapped_column(Integer)