from pydantic import BaseModel, create_model

from .registry import get_field_strategy
from .structure import FormStructure


def get_form_record_data_schema(structure: FormStructure) -> type[BaseModel]:
    fields: dict = {
        field.slug: get_field_strategy(field.category).get_pydentic_field(field)
        for field in structure
    }
    return create_model("FormRecordDataSchema", **fields)
