from typing import Generic, TypeVar

from pydantic import BaseModel

from backend.src.forms.types import FormFieldCategory

DefaultValueT = TypeVar("DefaultValueT")


class ParamsSchema(BaseModel, Generic[DefaultValueT]):
    required: bool
    help_text: str
    default_value: DefaultValueT


FormFieldCategoryT = TypeVar("FormFieldCategoryT", bound=FormFieldCategory)
FormFieldParamsSchemaT = TypeVar("FormFieldParamsSchemaT", bound=ParamsSchema)


class FormFieldSchema(BaseModel, Generic[FormFieldCategoryT, FormFieldParamsSchemaT]):
    slug: str
    label: str
    category: FormFieldCategoryT
    params: FormFieldParamsSchemaT
