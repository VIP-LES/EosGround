from sqlalchemy import Identity, Integer, ForeignKey, DOUBLE_PRECISION, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column

from EosGround.database.models import TableBase
from EosGround.database.models.eos import SCHEMA

class HealthReport(TableBase):
    __tablename__ = 'health_report'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True, init=False)
    packet_id: Mapped[int] = mapped_column(ForeignKey("eos_schema.received_packets.id"))
    # please check types to see if they are acceptable
    device_id: Mapped[int] = mapped_column(Enum)
    # please check types to see if they are acceptable
    health_report: Mapped[str] = mapped_column(Text)