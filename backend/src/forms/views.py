from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.permission import IsAuthenticated
from backend.src.dashboard import services as dashboard_services
from backend.src.database.dependencies import get_db
from backend.src.forms.dependencies import get_form, get_public_form
from backend.src.permissions.dependencies import PermissionsDependency
from backend.src.users.dependencies import get_current_user
from backend.src.users.models import User

from . import services as form_services
from .models import Form
from .schemas import (
    FormCreateSchema,
    FormDoesNotFound,
    FormPartialUpdateSchema,
    FormSchema,
    FormUpdateSchema,
    PublicFormSchema,
)

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    response_model=list[FormSchema],
)
async def get_forms(
    db_session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    dashboard_uuid: UUID | None = None,
) -> Any:
    if dashboard_uuid and dashboard_services.get_by_uuid(
        db_session=db_session, user_id=user.id, uuid=dashboard_uuid
    ):
        return await form_services.get_all_by_dashboard_uuid(
            db_session=db_session, user_id=user.id, dashboard_uuid=dashboard_uuid
        )

    return await form_services.get_all(db_session=db_session, user_id=user.id)


@router.post(
    "/",
    response_model=FormSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
)
async def create_form(
    data: FormCreateSchema,
    db_session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Any:
    if not dashboard_services.get_by_uuid(
        db_session=db_session, user_id=user.id, uuid=data.dashboard_uuid
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User doesn't have dashboard with uuid {data.dashboard_uuid}",
        )

    return await form_services.create(db_session=db_session, data=data)


@router.get(
    "/{uuid}",
    response_model=FormSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    responses={404: {"model": FormDoesNotFound, "description": "Form doesn't found."}},
)
async def get_specific_dashboard(form: Form = Depends(get_form)) -> Any:
    return form


@router.put(
    "/{uuid}",
    response_model=FormSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    responses={404: {"model": FormDoesNotFound, "description": "Form doesn't found."}},
)
async def update_form(
    data: FormUpdateSchema,
    db_session: AsyncSession = Depends(get_db),
    form: Form = Depends(get_form),
) -> Any:
    return await form_services.update(db_session=db_session, form=form, data=data)


@router.patch(
    "/{uuid}",
    response_model=FormSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    responses={404: {"model": FormDoesNotFound, "description": "Form doesn't found."}},
)
async def update_form_partial(
    data: FormPartialUpdateSchema,
    db_session: AsyncSession = Depends(get_db),
    form: Form = Depends(get_form),
) -> Any:
    return await form_services.update(db_session=db_session, form=form, data=data)


@router.delete(
    "/{uuid}",
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": FormDoesNotFound, "description": "Form doesn't found."}},
)
async def delete_form(
    db_session: AsyncSession = Depends(get_db), form: Form = Depends(get_form)
) -> None:
    await form_services.delete_by_uuid(db_session=db_session, uuid=form.uuid)


@router.get(
    "/public/{uuid}",
    response_model=PublicFormSchema,
    dependencies=[Depends(PermissionsDependency([]))],
    responses={404: {"model": FormDoesNotFound, "description": "Form doesn't found."}},
)
async def get_public_dashboard(form: Form = Depends(get_public_form)) -> Any:
    return form
