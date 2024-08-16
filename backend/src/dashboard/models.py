from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.database.core import Base

if TYPE_CHECKING:
    from backend.src.forms.models import Form
    from backend.src.users.models import User


class Dashboard(Base):
    uuid: Mapped[UUID] = mapped_column(default=uuid4, index=True, unique=True, primary_key=True)

    name: Mapped[str] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    user: Mapped["User"] = relationship(back_populates="dashboards")

    forms: Mapped[list["Form"]] = relationship(back_populates="dashboard")

    __tablename__ = "dashboards"
