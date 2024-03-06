from sqlalchemy import Identity, Integer, TIMESTAMP, ForeignKey, DOUBLE_PRECISION
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

from EosGround.database.models import TableBase
from EosGround.database.models.eos import SCHEMA

from EosLib.format.formats.position import FlightState

# Creates a model of the DownlinkCommand table and maps python types to their PostgreSQL counterparts


class DownlinkCommand(TableBase):
    __tablename__ = 'downlink_command'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True, init=False)
    packet_id: Mapped[int] = mapped_column(ForeignKey("eos_schema.received_packets.id"))
    file_id: Mapped[int] = mapped_column(Integer)
    num_chunks: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    missing_chunks:  Mapped[list[int]] = mapped_column(ARRAY(Integer))
