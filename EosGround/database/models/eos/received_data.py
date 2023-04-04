from sqlalchemy import Identity, Integer
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column

from EosGround.database.models import TableBase
from EosGround.database.models.eos import SCHEMA


class ReceivedData(TableBase):
    __tablename__ = 'received_data'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True, init=False)
    raw_bytes: Mapped[bytearray] = mapped_column(BYTEA)
    rssi: Mapped[int] = mapped_column(default=0)
    processed: Mapped[bool] = mapped_column(default=False)
