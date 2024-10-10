from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.dependencies import get_db
from backend.src.users.dependencies import get_current_user
from backend.src.users.models import User

from . import services as form_services
from .models import Form


async def get_form(
    db_session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    uuid: UUID = Path(...),
) -> Form:
    if instance := await form_services.get_by_uuid_and_user_id(
        db_session=db_session, user_id=user.id, uuid=uuid
    ):
        return instance
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Form with uuid {uuid} doesn't found."
    )


async def get_shared_form(
    db_session: AsyncSession = Depends(get_db),
    uuid: UUID = Path(...),
) -> Form:
    instance = await form_services.get_by_uuid(db_session=db_session, uuid=uuid)
    if instance and instance.shared:
        return instance

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Form with uuid {uuid} doesn't found."
    )
