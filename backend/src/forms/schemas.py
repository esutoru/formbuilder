from uuid import UUID

from pydantic import BaseModel


class FormDoesNotFound(BaseModel):
    detail: str


class FormSchema(BaseModel):
    uuid: UUID
    name: str
    description: str
    color: str
    is_active: bool
    dashboard_uuid: UUID


class PublicFormSchema(BaseModel):
    uuid: UUID
    name: str
    description: str
    color: str


class FormCreateSchema(BaseModel):
    name: str
    description: str
    color: str
    is_active: bool
    dashboard_uuid: UUID

    class Config:
        from_attributes = True


class FormUpdateSchema(BaseModel):
    name: str
    description: str
    color: str
    is_active: bool


class FormPartialUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    color: str | None = None
    is_active: bool | None = None
