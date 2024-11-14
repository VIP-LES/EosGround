from sqlalchemy import Identity, Integer, ForeignKey, DOUBLE_PRECISION, TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from EosGround.database.models import TableBase
from EosGround.database.models.eos import SCHEMA

import datetime

class Telemetry(TableBase):
    __tablename__ = 'telemetry'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True, init=False)
    packet_id: Mapped[int] = mapped_column(ForeignKey("eos_schema.received_packets.id"))
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP)  # FIXME
    temperature: Mapped[float] = mapped_column(DOUBLE_PRECISION)
    pressure: Mapped[float] = mapped_column(DOUBLE_PRECISION)
    humidity: Mapped[float] = mapped_column(DOUBLE_PRECISION)
    x_rotation:  Mapped[float] = mapped_column(DOUBLE_PRECISION)
    y_rotation: Mapped[float] = mapped_column(DOUBLE_PRECISION)
    z_rotation: Mapped[float] = mapped_column(DOUBLE_PRECISION)
