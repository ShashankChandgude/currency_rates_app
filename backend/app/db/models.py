from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import declarative_base, relationship

if TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeBase

    Base = DeclarativeBase
else:
    Base = declarative_base()


class Currency(Base):
    __tablename__ = "currencies"
    code = Column(String(3), primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relationships
    base_rates = relationship(
        "Rate", back_populates="base_currency", foreign_keys="Rate.base_code"
    )
    quote_rates = relationship(
        "Rate", back_populates="quote_currency", foreign_keys="Rate.quote_code"
    )


class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

    rates = relationship("Rate", back_populates="provider")


class Rate(Base):
    __tablename__ = "rates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, nullable=False)
    base_code = Column(String(3), ForeignKey("currencies.code"), nullable=False)
    quote_code = Column(String(3), ForeignKey("currencies.code"), nullable=False)
    value = Column(Numeric(precision=18, scale=8), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)

    # Relationships
    base_currency = relationship(
        "Currency", foreign_keys=[base_code], back_populates="base_rates"
    )
    quote_currency = relationship(
        "Currency", foreign_keys=[quote_code], back_populates="quote_rates"
    )
    provider = relationship("Provider", back_populates="rates")
