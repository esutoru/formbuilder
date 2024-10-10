from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from .schemas import FormFieldSchema

TFormFieldSchema = TypeVar("TFormFieldSchema", bound=FormFieldSchema)
PydenticField = tuple[Any, Any]


class FieldStrategy(ABC, Generic[TFormFieldSchema]):
    @abstractmethod
    def get_pydentic_field(self, field: TFormFieldSchema) -> PydenticField:
        """
        Return pydentic field data. Used to create dynamic model for form models.

        Example:
        (str, Field(..., default="Foo", min_length=2))
        """
