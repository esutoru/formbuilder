from typing import Annotated, Any
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
    shared: bool
    dashboard_uuid: UUID
    structure: FormStructure

    class Config:
        from_attributes = True


class SharedFormSchema(BaseModel):
    uuid: UUID
    name: NameField
    description: str
    color: str
    structure: FormStructure


class FormCreateSchema(BaseModel):
    name: NameField
    description: str
    color: str
    shared: bool
    dashboard_uuid: UUID
    structure: FormStructure

    class Config:
        from_attributes = True


class FormUpdateSchema(BaseModel):
    name: NameField
    description: str
    color: str
    shared: bool
    structure: FormStructure


class FormPartialUpdateSchema(BaseModel):
    name: OptionalNameField
    description: str | None = None
    color: str | None = None
    shared: bool | None = None
    structure: FormStructure | None = None


class FormRecordSchema(BaseModel):
    uuid: UUID
    form_uuid: UUID
    data: dict[str, Any]


class FormRecordCreateSchema(BaseModel):
    form_uuid: UUID
    data: dict[str, Any]


class CreateFormRecordResponseSchema(BaseModel):
    success: bool
