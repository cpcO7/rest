from sqlalchemy import BigInteger, VARCHAR, BOOLEAN
from sqlalchemy.orm import mapped_column, Mapped

from apps.models import User as appUser
from tlg_bot.db.base import Base, AbstractClass


class User(Base, AbstractClass):

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(150), nullable=True)
    last_name: Mapped[str] = mapped_column(VARCHAR(150), nullable=True)
    email: Mapped[str] = mapped_column(VARCHAR(254), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(VARCHAR(128), nullable=True)

    username: Mapped[str] = mapped_column(VARCHAR(150), nullable=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR(20), nullable=True)
    type: Mapped[str] = mapped_column(VARCHAR(20), default=appUser.Type.STUDENT)
    is_staff: Mapped[bool] = mapped_column(BOOLEAN, default=False)
