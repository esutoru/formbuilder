from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.database.core import Base

if TYPE_CHECKING:
    from backend.src.users.models import Dashboard


class Form(Base):
    uuid: Mapped[UUID] = mapped_column(default=uuid4, index=True, unique=True, primary_key=True)

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    color: Mapped[str] = mapped_column()

    is_active: Mapped[bool] = mapped_column(default=False)

    dashboard_uuid: Mapped[UUID] = mapped_column(ForeignKey("dashboards.uuid"), index=True)
    dashboard: Mapped["Dashboard"] = relationship(back_populates="forms")

    structure: Mapped[list] = mapped_column(type_=JSON, nullable=True)

    __tablename__ = "forms"
