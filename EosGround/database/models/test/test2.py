from sqlalchemy import BigInteger, Identity, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from EosGround.database.models import TableBase
from EosGround.database.models.test import SCHEMA
from EosGround.database.models.test.test1 import Test1


class Test2(TableBase):
    __tablename__ = 'test2'
    __table_args__ = {'schema': SCHEMA}

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True, init=False)
    random_number: Mapped[int | None]
    test1_id: Mapped[int | None] = mapped_column(ForeignKey("test_schema.test1.id"))
    test1: Mapped[Test1 | None] = relationship(init=False, default=None)
