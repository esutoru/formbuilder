from pydantic import Field
from pydantic_core import PydanticUndefined

from backend.src.forms.structure.base import FieldStrategy, PydenticField

from .schemas import TextAreaFormFieldSchema


class TextAreaFieldStrategy(FieldStrategy[TextAreaFormFieldSchema]):
    def get_pydentic_field(self, field: TextAreaFormFieldSchema) -> PydenticField:
        return (
            str if field.params.required else str | None,
            Field(
                default=(
                    PydanticUndefined
                    if field.params.default_value is None
                    else field.params.default_value
                ),
                min_length=field.params.min_length,
                max_length=field.params.max_length,
            ),
        )
