from pydantic import Field
from pydantic_core import PydanticUndefined

from backend.src.forms.structure.base import FieldStrategy, PydenticField

from .schemas import BooleanFormFieldSchema


class BooleanFieldStrategy(FieldStrategy[BooleanFormFieldSchema]):
    def get_pydentic_field(self, field: BooleanFormFieldSchema) -> PydenticField:
        return (
            bool if field.params.required else bool | None,
            Field(
                default=(
                    PydanticUndefined
                    if field.params.default_value is None
                    else field.params.default_value
                ),
            ),
        )
