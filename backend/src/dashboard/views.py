from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.permission import IsAuthenticated
from backend.src.dashboard.dependencies import get_dashboard
from backend.src.dashboard.models import Dashboard
from backend.src.dashboard.schemas import (
    DashboardCreateSchema,
    DashboardDoesNotFound,
    DashboardPartialUpdateSchema,
    DashboardSchema,
    DashboardUpdateSchema,
)
from backend.src.database.dependencies import get_db
from backend.src.forms import services as form_services
from backend.src.permissions.dependencies import PermissionsDependency
from backend.src.users.dependencies import get_current_user
from backend.src.users.models import User

from . import services as dashboard_services

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    response_model=list[DashboardSchema],
)
async def get_dashboards(
    db_session: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
) -> Any:
    return await dashboard_services.get_all_by_user_id(db_session=db_session, user_id=user.id)


@router.post(
    "/",
    response_model=DashboardSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
)
async def add_dashboard(
    data: DashboardCreateSchema,
    db_session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Any:
    return await dashboard_services.create_dashboard(
        db_session=db_session, user_id=user.id, data=data
    )


@router.get(
    "/{uuid}",
    response_model=DashboardSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    responses={404: {"model": DashboardDoesNotFound, "description": "Dashboard doesn't found."}},
)
async def get_specific_dashboard(dashboard: Dashboard = Depends(get_dashboard)) -> Any:
    return dashboard


@router.put(
    "/{uuid}",
    response_model=DashboardSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    responses={404: {"model": DashboardDoesNotFound, "description": "Dashboard doesn't found."}},
)
async def update_dashboard(
    data: DashboardUpdateSchema,
    db_session: AsyncSession = Depends(get_db),
    dashboard: Dashboard = Depends(get_dashboard),
) -> Any:
    return await dashboard_services.update_dashboard(
        db_session=db_session, dashboard=dashboard, data=data
    )


@router.patch(
    "/{uuid}",
    response_model=DashboardSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    responses={404: {"model": DashboardDoesNotFound, "description": "Dashboard doesn't found."}},
)
async def update_dashboard_partial(
    data: DashboardPartialUpdateSchema,
    db_session: AsyncSession = Depends(get_db),
    dashboard: Dashboard = Depends(get_dashboard),
) -> Any:
    return await dashboard_services.update_dashboard(
        db_session=db_session, dashboard=dashboard, data=data
    )


@router.delete(
    "/{uuid}",
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": DashboardDoesNotFound, "description": "Dashboard doesn't found."}},
)
async def delete_dashboard(
    db_session: AsyncSession = Depends(get_db), dashboard: Dashboard = Depends(get_dashboard)
) -> None:
    await form_services.delete_all_records_by_dashboard_uuid(
        db_session=db_session, dashboard_uuid=dashboard.uuid
    )
    await form_services.delete_all_by_dashboard_uuid(
        db_session=db_session, dashboard_uuid=dashboard.uuid
    )
    await dashboard_services.delete_by_uuid(db_session=db_session, uuid=dashboard.uuid)
