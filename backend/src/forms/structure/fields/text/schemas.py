from typing import Literal

from backend.src.forms.structure.schemas import FormFieldSchema, ParamsSchema


class TextParamsSchema(ParamsSchema[str]):
    min_length: int
    max_length: int


class TextFormFieldSchema(FormFieldSchema[Literal["text"], TextParamsSchema]):
    pass
