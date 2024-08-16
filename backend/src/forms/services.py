from typing import Sequence
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.dashboard.models import Dashboard
from backend.src.forms.schemas import (
    FormCreateSchema,
    FormPartialUpdateSchema,
    FormUpdateSchema,
)

from .models import Form


async def get_all(*, db_session: AsyncSession, user_id: int) -> Sequence[Form]:
    result = await db_session.execute(
        select(Form).join(Dashboard).filter(Dashboard.user_id == user_id)
    )
    return result.scalars().all()


async def get_all_by_dashboard_uuid(
    *, db_session: AsyncSession, user_id: int, dashboard_uuid: UUID
) -> Sequence[Form]:
    result = await db_session.execute(
        select(Form)
        .join(Dashboard)
        .filter(Dashboard.user_id == user_id, Form.dashboard_uuid == dashboard_uuid)
    )
    return result.scalars().all()


async def get_by_uuid(*, db_session: AsyncSession, uuid: UUID) -> Form | None:
    result = await db_session.execute(
        select(Form).filter(
            Form.uuid == uuid,
        )
    )
    return result.scalars().one_or_none()


async def get_by_uuid_and_user_id(
    *, db_session: AsyncSession, uuid: UUID, user_id: int
) -> Form | None:
    result = await db_session.execute(
        select(Form)
        .join(Dashboard)
        .filter(
            Dashboard.user_id == user_id,
            Form.uuid == uuid,
        )
    )
    return result.scalars().one_or_none()


async def create(*, db_session: AsyncSession, data: FormCreateSchema) -> Form:
    instance = Form(**data.model_dump(exclude_unset=True))
    db_session.add(instance)
    await db_session.commit()
    await db_session.refresh(instance)
    return instance


async def update(
    *,
    db_session: AsyncSession,
    form: Form,
    data: FormUpdateSchema | FormPartialUpdateSchema,
) -> Form:
    update_data = data.model_dump(exclude_none=True)
    if not update_data:
        return form

    for field in update_data:
        setattr(form, field, update_data[field])

    await db_session.commit()
    await db_session.refresh(form)

    return form


async def delete_by_uuid(*, db_session: AsyncSession, uuid: UUID) -> None:
    await db_session.execute(delete(Form).where(Form.uuid == uuid))
    await db_session.commit()


async def delete_all_by_dashboard_uuid(*, db_session: AsyncSession, dashboard_uuid: UUID) -> None:
    await db_session.execute(delete(Form).where(Form.dashboard_uuid == dashboard_uuid))
    await db_session.commit()
