from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.database.core import Base
from backend.src.database.mixins import TimeStampMixin

if TYPE_CHECKING:
    from backend.src.dashboard.models import Dashboard


class User(Base, TimeStampMixin):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str] = mapped_column(default="")
    last_name: Mapped[str] = mapped_column(default="")

    password: Mapped[str] = mapped_column(default="")
    is_active: Mapped[bool] = mapped_column(default=True)

    dashboards: Mapped[list["Dashboard"]] = relationship(back_populates="user")

    __tablename__ = "users"
