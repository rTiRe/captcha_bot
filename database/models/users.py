from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from .meta import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True)


class Admin(Base):
    __tablename__ = 'admins'
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True)