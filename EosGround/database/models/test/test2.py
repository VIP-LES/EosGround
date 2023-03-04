from sqlalchemy import BigInteger, Column, Identity, Integer
from sqlalchemy.orm import declarative_base

from EosGround.database.models.test import SCHEMA


class Test2(declarative_base()):
    __tablename__ = 'test2'
    __table_args__ = {'schema': SCHEMA}
    id = Column(BigInteger, Identity(start=1), nullable=False, primary_key=True)
    random_number = Column(Integer, nullable=True)
