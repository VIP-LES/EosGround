from sqlalchemy import Identity, Integer
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from EosGround.database.models import TableBase
from EosGround.database.models.eos import SCHEMA
from sqlalchemy import TIMESTAMP


class ReceivedData(TableBase):
    __tablename__ = 'received_data'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True, init=False)
    raw_bytes: Mapped[bytes] = mapped_column(BYTEA)
    rssi: Mapped[int] = mapped_column()
    received_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    processed: Mapped[bool] = mapped_column(default=False)
