from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.dashboard import services as dashboard_services
from backend.src.dashboard.models import Dashboard
from backend.src.database.dependencies import get_db
from backend.src.users.dependencies import get_current_user
from backend.src.users.models import User


async def get_dashboard(
    db_session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    uuid: UUID = Path(...),
) -> Dashboard:
    if dashboard := await dashboard_services.get_by_uuid(
        db_session=db_session, user_id=user.id, uuid=uuid
    ):
        return dashboard
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Dashboard with uuid {uuid} doesn't found."
    )
