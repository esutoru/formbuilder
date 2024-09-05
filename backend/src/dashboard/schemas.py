from uuid import UUID

from pydantic import BaseModel, Field


class DashboardDoesNotFound(BaseModel):
    detail: str


class DashboardSchema(BaseModel):
    uuid: UUID
    name: str = Field(min_length=3)


class DashboardCreateSchema(BaseModel):
    name: str = Field(min_length=3)

    class Config:
        from_attributes = True


class DashboardUpdateSchema(BaseModel):
    name: str = Field(min_length=3)


class DashboardPartialUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=3)
