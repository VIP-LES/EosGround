from sqlalchemy import Identity, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column

from EosGround.database.models import TableBase
from EosGround.database.models.eos import SCHEMA

# Creates a model of the DownlinkChunk table and maps python types to their PostgreSQL counterparts


class DownlinkChunk(TableBase):
    __tablename__ = 'downlink_chunk'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True, init=False)
    packet_id: Mapped[int] = mapped_column(ForeignKey("eos_schema.received_packets.id"))
    chunk_num: Mapped[int] = mapped_column(Integer)
    chunk_body: Mapped[bytes] = mapped_column(BYTEA)
