from sqlalchemy import BigInteger, Identity
from sqlalchemy.orm import Mapped, mapped_column

from EosGround.database.models import TableBase
from EosGround.database.models.test import SCHEMA


class Test1(TableBase):
    __tablename__ = 'test1'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True, init=False)
    random_number: Mapped[int | None]
    processed: Mapped[bool] = mapped_column(default=False)
