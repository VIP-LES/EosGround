from sqlalchemy import Identity, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from EosGround.database.models import TableBase
from EosGround.database.models.eos import SCHEMA


class TerminalOutput(TableBase):
    __tablename__ = 'terminal_output'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True, init=False)
    received_packets_id: Mapped[bytes] = mapped_column(ForeignKey("eos_schema.received_packets.id"))
    transmit_table_id: Mapped[int] = mapped_column(ForeignKey("eos_schema.transmit_table.id"))
    terminal_output: Mapped[str] = mapped_column(Text)