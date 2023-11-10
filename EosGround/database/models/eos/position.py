from sqlalchemy import Identity, Integer, TIMESTAMP, ForeignKey, DOUBLE_PRECISION
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from EosGround.database.models import TableBase
from EosGround.database.models.eos import SCHEMA

from EosLib.format.formats.position import FlightState

# Creates a model of the Position table and maps python types to their PostgreSQL counterparts
#describes what the table looks like in code


class Position(TableBase):
    __tablename__ = 'position'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True, init=False)
    packet_id: Mapped[int] = mapped_column(ForeignKey("eos_schema.received_packets.id"))
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP)
    latitude: Mapped[float] = mapped_column(DOUBLE_PRECISION)
    longitude: Mapped[float] = mapped_column(DOUBLE_PRECISION)
    altitude: Mapped[float] = mapped_column(DOUBLE_PRECISION)
    speed:  Mapped[float] = mapped_column(DOUBLE_PRECISION)
    num_satellites: Mapped[int] = mapped_column(Integer)
    flight_state: Mapped[FlightState] = mapped_column(Integer)
