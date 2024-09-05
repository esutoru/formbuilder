from typing import Annotated, Union

from pydantic.functional_validators import AfterValidator

from .fields.boolean import BooleanFormFieldSchema
from .fields.text import TextFormFieldSchema
from .fields.text_area import TextAreaFormFieldSchema
from .validators import (
    check_fields_count,
    check_labels_uniqueness,
    check_slugs_uniqueness,
)

FormStructureItem = Union[BooleanFormFieldSchema, TextFormFieldSchema, TextAreaFormFieldSchema]
FormStructure = Annotated[
    list[FormStructureItem],
    AfterValidator(check_slugs_uniqueness),
    AfterValidator(check_labels_uniqueness),
    AfterValidator(check_labels_uniqueness),
    AfterValidator(check_fields_count),
]
