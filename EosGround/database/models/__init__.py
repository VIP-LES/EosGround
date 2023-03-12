from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class TableBase(MappedAsDataclass, DeclarativeBase):
    pass
