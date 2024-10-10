from typing import Mapping

from backend.src.forms.types import FormFieldCategory

from .base import FieldStrategy
from .fields.boolean.strategy import BooleanFieldStrategy
from .fields.text.strategy import TextFieldStrategy
from .fields.text_area.strategy import TextAreaFieldStrategy

CATEGORY_TO_STRATEGY: Mapping[FormFieldCategory, FieldStrategy] = {
    "text": TextFieldStrategy(),
    "text_area": TextAreaFieldStrategy(),
    "boolean": BooleanFieldStrategy(),
}


def get_field_strategy(category: FormFieldCategory) -> FieldStrategy:
    return CATEGORY_TO_STRATEGY[category]
