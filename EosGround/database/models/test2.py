from sqlalchemy import BigInteger, Column, Integer, Sequence
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Test2(Base):
    __tablename__ = "test2"
    __table_args__ = {'schema': 'eos_schema'}
    id = Column(BigInteger, Sequence("test2_id_seq", schema="eos_schema"), nullable=False, primary_key=True)
    random_number = Column(Integer, nullable=True)
