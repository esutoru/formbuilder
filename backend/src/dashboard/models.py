from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.database.core import Base

if TYPE_CHECKING:
    from backend.src.users.models import User


class Dashboard(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    uuid: Mapped[UUID] = mapped_column(unique=True, default=uuid4, index=True)

    name: Mapped[str] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    user: Mapped["User"] = relationship(back_populates="dashboards")

    __tablename__ = "dashboards"
