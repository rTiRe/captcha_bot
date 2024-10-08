from sqlalchemy import Boolean, Integer, PickleType
from sqlalchemy.orm import Mapped, mapped_column

from .meta import Base


class BaseMessage:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    message: Mapped[dict | None] = mapped_column(PickleType, nullable=True)
    added_by: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)


class WelcomeMessage(BaseMessage, Base):
    __tablename__ = 'welcome_messages'


class CaptchaMessage(BaseMessage, Base):
    __tablename__ = 'captcha_messages'


class CaptchaButton(BaseMessage, Base):
    __tablename__ = 'captcha_buttons'


class HelloMessage(BaseMessage, Base):
    __tablename__ = 'hello_messages'

class TimeoutMessage(BaseMessage, Base):
    __tablename__ = 'timeout_messages'