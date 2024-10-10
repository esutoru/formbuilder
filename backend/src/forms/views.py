from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.permission import IsAuthenticated
from backend.src.dashboard import services as dashboard_services
from backend.src.database.dependencies import get_db
from backend.src.forms.dependencies import get_form, get_shared_form
from backend.src.forms.helpers import get_deleted_field_slugs
from backend.src.forms.structure.record import get_form_record_data_schema
from backend.src.permissions.dependencies import PermissionsDependency
from backend.src.users.dependencies import get_current_user
from backend.src.users.models import User

from . import services as form_services
from .models import Form
from .schemas import (
    CreateFormRecordResponseSchema,
    FormCreateSchema,
    FormDoesNotFound,
    FormPartialUpdateSchema,
    FormRecordCreateSchema,
    FormRecordSchema,
    FormSchema,
    FormUpdateSchema,
    SharedFormSchema,
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
    current_structure = FormSchema.model_validate(form).structure
    new_structure = data.structure or current_structure
    if deleted_field_slugs := get_deleted_field_slugs(current_structure, new_structure):
        await form_services.omit_fields_from_form_records_data(
            db_session=db_session, form_uuid=form.uuid, fields=deleted_field_slugs
        )

    return await form_services.update_form(db_session=db_session, form=form, data=data)


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
    current_structure = FormSchema.model_validate(form).structure
    new_structure = data.structure or current_structure
    if deleted_field_slugs := get_deleted_field_slugs(current_structure, new_structure):
        await form_services.omit_fields_from_form_records_data(
            db_session=db_session, form_uuid=form.uuid, fields=deleted_field_slugs
        )

    return await form_services.update_form(db_session=db_session, form=form, data=data)


@router.delete(
    "/{uuid}",
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": FormDoesNotFound, "description": "Form doesn't found."}},
)
async def delete_form(
    db_session: AsyncSession = Depends(get_db), form: Form = Depends(get_form)
) -> None:
    await form_services.delete_all_records_by_form_uuid(db_session=db_session, form_uuid=form.uuid)
    await form_services.delete_by_uuid(db_session=db_session, uuid=form.uuid)


@router.get(
    "/shared/{uuid}",
    response_model=SharedFormSchema,
    dependencies=[Depends(PermissionsDependency([]))],
    responses={404: {"model": FormDoesNotFound, "description": "Form doesn't found."}},
)
async def get_shared_form_instance(form: Form = Depends(get_shared_form)) -> Any:
    return form


@router.post(
    "/shared/{uuid}/fill",
    response_model=CreateFormRecordResponseSchema,
    dependencies=[Depends(PermissionsDependency([]))],
)
async def fill_form(
    record_data: dict[str, Any],
    db_session: AsyncSession = Depends(get_db),
    form: Form = Depends(get_shared_form),
) -> Any:
    try:
        get_form_record_data_schema(FormSchema.model_validate(form).structure)(**record_data)
    except ValidationError as exc:
        raise HTTPException(
            status_code=400,
            detail=exc.errors(
                include_url=False,
                include_input=False,
            ),
        )

    await form_services.create_form_record(
        db_session=db_session, data=FormRecordCreateSchema(form_uuid=form.uuid, data=record_data)
    )

    return JSONResponse({"success": True}, status_code=status.HTTP_201_CREATED)


@router.get(
    "/{uuid}/records",
    response_model=list[FormRecordSchema],
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    responses={404: {"model": FormDoesNotFound, "description": "Form doesn't found."}},
)
async def get_form_records(form: Form = Depends(get_form)) -> Any:
    return await form.awaitable_attrs.records
