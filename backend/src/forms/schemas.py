from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from backend.src.forms.structure.structure import FormStructure

NameField = Annotated[str, Field(min_length=3)]
OptionalNameField = Annotated[str | None, Field(None, min_length=3)]


class FormDoesNotFound(BaseModel):
    detail: str


class FormSchema(BaseModel):
    uuid: UUID
    name: NameField
    description: str
    color: str
    is_active: bool
    dashboard_uuid: UUID
    structure: FormStructure


class PublicFormSchema(BaseModel):
    uuid: UUID
    name: NameField
    description: str
    color: str


class FormCreateSchema(BaseModel):
    name: NameField
    description: str
    color: str
    is_active: bool
    dashboard_uuid: UUID
    structure: FormStructure

    class Config:
        from_attributes = True


class FormUpdateSchema(BaseModel):
    name: NameField
    description: str
    color: str
    is_active: bool
    structure: FormStructure


class FormPartialUpdateSchema(BaseModel):
    name: OptionalNameField
    description: str | None = None
    color: str | None = None
    is_active: bool | None = None
    structure: FormStructure | None = None
