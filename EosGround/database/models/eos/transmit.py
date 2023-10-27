from sqlalchemy import Identity, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import BYTEA

from EosGround.database.models import TableBase
from EosGround.database.models.eos import SCHEMA
from sqlalchemy import TIMESTAMP
from datetime import datetime


class Transmit(TableBase):
    __tablename__ = 'transmit_table'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True, init=False)
    time_sent: Mapped[datetime] = mapped_column(TIMESTAMP)
    packet_type: Mapped[int] = mapped_column()
    sender: Mapped[int] = mapped_column()
    priority: Mapped[int] = mapped_column()
    destination: Mapped[int] = mapped_column()
    generate_time: Mapped[int] = mapped_column()
    body: Mapped[str] = mapped_column(BYTEA)

