from sqlalchemy import Identity, Integer, TIMESTAMP, REAL, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from EosGround.database.models import TableBase
from EosGround.database.models.eos import SCHEMA

from EosLib.format.position import FlightState


class Position(TableBase):
    __tablename__ = 'position'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True, init=False)
    packet_id: Mapped[int | None] = mapped_column(ForeignKey("eos_schema.received_packets.id"))
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP)
    latitude: Mapped[float] = mapped_column(REAL)
    longitude: Mapped[float] = mapped_column(REAL)
    altitude: Mapped[float] = mapped_column(REAL)
    speed:  Mapped[float] = mapped_column(REAL)
    num_satellites: Mapped[int] = mapped_column(Integer)
    flight_state: Mapped[FlightState] = mapped_column(Integer)
