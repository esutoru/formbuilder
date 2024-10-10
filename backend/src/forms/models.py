from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.database.core import Base

if TYPE_CHECKING:
    from backend.src.users.models import Dashboard


class Form(Base):
    uuid: Mapped[UUID] = mapped_column(default=uuid4, index=True, unique=True, primary_key=True)

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    color: Mapped[str] = mapped_column()

    shared: Mapped[bool] = mapped_column(default=False)

    dashboard_uuid: Mapped[UUID] = mapped_column(ForeignKey("dashboards.uuid"), index=True)
    dashboard: Mapped["Dashboard"] = relationship(back_populates="forms")

    records: Mapped[list["FormRecord"]] = relationship(back_populates="form")

    structure: Mapped[list] = mapped_column(type_=JSON)

    __tablename__ = "forms"


class FormRecord(Base):
    uuid: Mapped[UUID] = mapped_column(default=uuid4, index=True, unique=True, primary_key=True)

    form_uuid: Mapped[UUID] = mapped_column(ForeignKey("forms.uuid"), index=True)
    form: Mapped["Form"] = relationship(back_populates="records")

    data: Mapped[dict] = mapped_column(type_=JSONB)

    __tablename__ = "form_records"
