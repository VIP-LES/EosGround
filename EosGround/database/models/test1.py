from sqlalchemy import BigInteger, Boolean, Column, Integer, Sequence
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Test1(Base):
    __tablename__ = "test1"
    __table_args__ = {'schema': 'eos_schema'}
    id = Column(BigInteger, Sequence("test1_id_seq", schema="eos_schema"), nullable=False, primary_key=True)
    random_number = Column(Integer, nullable=True)
    processed = Column(Boolean, nullable=False)
