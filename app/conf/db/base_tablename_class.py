from typing import Any

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

#
# class BaseWithId(Base):
#
#     @declared_attr
#     def id(cls):
#         return Column(Integer, primary_key=True, autoincrement=True)
