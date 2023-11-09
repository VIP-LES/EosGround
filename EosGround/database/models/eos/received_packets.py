from sqlalchemy import Identity, Integer, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.dialects.postgresql import BYTEA


from EosGround.database.models import TableBase
from EosGround.database.models.eos import SCHEMA

class ReceivedPackets(TableBase):
    __tablename__ = 'received_packets'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True, init=False)
    generate_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    send_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    received_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    packet_body: Mapped[bytes] = mapped_column(BYTEA)
    data_id: Mapped[int] = mapped_column()
    packet_type: Mapped[int] = mapped_column()
    sender: Mapped[int] = mapped_column()
    priority: Mapped[int] = mapped_column()
    destination: Mapped[int] = mapped_column()
    sequence_number: Mapped[int] = mapped_column()
    processed: Mapped[bool] = mapped_column(default=False)
