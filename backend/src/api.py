from fastapi import APIRouter

from backend.src.auth.views import router as auth_router
from backend.src.dashboard.views import router as dashboard_router
from backend.src.forms.views import router as forms_router
from backend.src.users.views import router as users_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(dashboard_router, prefix="/dashboards", tags=["Dashboard"])
api_router.include_router(forms_router, prefix="/forms", tags=["Forms"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
