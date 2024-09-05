from typing import Literal

from backend.src.forms.structure.schemas import FormFieldSchema, ParamsSchema


class TextAreaParamsSchema(ParamsSchema[str]):
    min_length: int
    max_length: int


class TextAreaFormFieldSchema(FormFieldSchema[Literal["text_area"], TextAreaParamsSchema]):
    pass
