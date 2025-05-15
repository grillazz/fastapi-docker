from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, func
import enum
from datetime import datetime

from typing import Any

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    id: Any
    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


class TaxiStatus(enum.Enum):
    AVAILABLE = "available"
    BUSY = "busy"


class TripStatus(enum.Enum):
    ASSIGNED = "assigned"
    PICKING_UP = "picking_up"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Taxi(Base):
    __tablename__ = "taxis"

    taxi_id = Column(String, primary_key=True)
    status = Column(String, default=TaxiStatus.AVAILABLE.value)
    x = Column(Integer)
    y = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# class Trip(Base):
#     __tablename__ = "trips"
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(String, nullable=False)
#     taxi_id = Column(String, ForeignKey("taxis.taxi_id"))
#     start_x = Column(Integer, nullable=False)
#     start_y = Column(Integer, nullable=False)
#     end_x = Column(Integer, nullable=False)
#     end_y = Column(Integer, nullable=False)
#     status = Column(String, default=TripStatus.ASSIGNED.value)
#     created_at = Column(DateTime, default=func.now())
#     pickup_at = Column(DateTime, nullable=True)
#     completed_at = Column(DateTime, nullable=True)
#     wait_time = Column(Float, nullable=True)  # In minutes
#     travel_time = Column(Float, nullable=True)  # In minutes
