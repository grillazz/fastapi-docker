from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum,
    func,
)
import enum
from datetime import datetime

from typing import Any

from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import func
from sqlalchemy.future import select


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

    # TODO: this can iterate over all taxis and find the closest one which is available
    @classmethod
    async def find_closest_and_lock_it(cls, async_session, x: int, y: int):
        distance = func.sqrt(func.pow(cls.x - x, 2) + func.pow(cls.y - y, 2))
        stmt = (
            select(cls)
            .where(cls.status == TaxiStatus.AVAILABLE.value)
            .order_by(distance)
            .limit(1)
        )

        result = await async_session.execute(stmt)
        closest_taxi = result.scalars().first()

        if closest_taxi:
            closest_taxi.status = TaxiStatus.BUSY.value
            await async_session.flush()

        return closest_taxi


class Trip(Base):
    __tablename__ = "trips"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(String, nullable=False)
    taxi_id = Column(String, ForeignKey("taxis.taxi_id"))
    start_x = Column(Integer, nullable=False)
    start_y = Column(Integer, nullable=False)
    end_x = Column(Integer, nullable=False)
    end_y = Column(Integer, nullable=False)
    status = Column(String, default=TripStatus.ASSIGNED.value)
