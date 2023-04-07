from sqlalchemy import Identity, Integer, TIMESTAMP, REAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from EosGround.database.models import TableBase
from EosGround.database.models.eos import SCHEMA


class Telemetry(TableBase):
    __tablename__ = 'telemetry'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True, init=False)
    packet_id: Mapped[int] = mapped_column(ForeignKey("eos_schema.received_packets.id"))
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP)
    temperature: Mapped[float] = mapped_column(REAL)
    pressure: Mapped[float] = mapped_column(REAL)
    humidity: Mapped[float] = mapped_column(REAL)
    x_rotation:  Mapped[float] = mapped_column(REAL)
    y_rotation: Mapped[float] = mapped_column(REAL)
    z_rotation: Mapped[float] = mapped_column(REAL)
