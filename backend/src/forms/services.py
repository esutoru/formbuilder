from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.dashboard.models import Dashboard
from backend.src.forms.schemas import (
    FormCreateSchema,
    FormPartialUpdateSchema,
    FormRecordCreateSchema,
    FormUpdateSchema,
)

from .models import Form, FormRecord


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


async def update_form(
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


async def create_form_record(
    *, db_session: AsyncSession, data: FormRecordCreateSchema
) -> FormRecord:
    instance = FormRecord(**data.model_dump(exclude_unset=True))
    db_session.add(instance)
    await db_session.commit()
    await db_session.refresh(instance)
    return instance


async def delete_all_records_by_dashboard_uuid(
    *, db_session: AsyncSession, dashboard_uuid: UUID
) -> None:
    await db_session.execute(
        delete(FormRecord)
        .where(FormRecord.form_uuid == Form.uuid)
        .where(Form.dashboard_uuid == dashboard_uuid)
    )
    await db_session.commit()


async def delete_all_records_by_form_uuid(*, db_session: AsyncSession, form_uuid: UUID) -> None:
    await db_session.execute(delete(FormRecord).where(FormRecord.form_uuid == form_uuid))
    await db_session.commit()


async def omit_fields_from_form_records_data(
    *, db_session: AsyncSession, form_uuid: UUID, fields: Sequence[str]
) -> None:
    new_value: Any = FormRecord.data
    for field in fields:
        new_value = new_value.op("-")(field)

    await db_session.execute(
        update(FormRecord)
        .where(FormRecord.form_uuid == form_uuid)
        .values({FormRecord.data: new_value})
    )
    await db_session.commit()
