from uuid import UUID

from pydantic import BaseModel


class DashboardDoesNotFound(BaseModel):
    detail: str


class DashboardSchema(BaseModel):
    uuid: UUID
    name: str


class DashboardCreateSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class DashboardUpdateSchema(BaseModel):
    name: str


class DashboardPartialUpdateSchema(BaseModel):
    name: str | None = None
