from typing import Sequence
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.dashboard.models import Dashboard
from backend.src.dashboard.schemas import (
    DashboardCreateSchema,
    DashboardPartialUpdateSchema,
    DashboardUpdateSchema,
)


async def get_all_by_user_id(*, db_session: AsyncSession, user_id: int) -> Sequence[Dashboard]:
    result = await db_session.execute(select(Dashboard).filter(Dashboard.user_id == user_id))
    return result.scalars().all()


async def get_by_uuid(*, db_session: AsyncSession, user_id: int, uuid: UUID) -> Dashboard | None:
    result = await db_session.execute(
        select(Dashboard).filter(
            Dashboard.user_id == user_id,
            Dashboard.uuid == uuid,
        )
    )
    return result.scalars().one_or_none()


async def create_dashboard(
    *, db_session: AsyncSession, user_id: int, data: DashboardCreateSchema
) -> Dashboard:
    dashboard = Dashboard(user_id=user_id, **data.model_dump(exclude_unset=True))
    db_session.add(dashboard)
    await db_session.commit()
    await db_session.refresh(dashboard)
    return dashboard


async def update_dashboard(
    *,
    db_session: AsyncSession,
    dashboard: Dashboard,
    data: DashboardUpdateSchema | DashboardPartialUpdateSchema,
) -> Dashboard:
    update_data = data.model_dump(exclude_none=True)
    if not update_data:
        return dashboard

    for field in update_data:
        setattr(dashboard, field, update_data[field])

    await db_session.commit()
    await db_session.refresh(dashboard)

    return dashboard


async def delete_by_uuid(*, db_session: AsyncSession, uuid: UUID) -> None:
    await db_session.execute(delete(Dashboard).where(Dashboard.uuid == uuid))
    await db_session.commit()
