from typing import Literal

from backend.src.forms.structure.schemas import FormFieldSchema, ParamsSchema


class BooleanParamsSchema(ParamsSchema[bool]):
    display_format: Literal["check", "star", "toggle"]


class BooleanFormFieldSchema(FormFieldSchema[Literal["boolean"], BooleanParamsSchema]):
    pass
