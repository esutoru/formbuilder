from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .structure import FormStructureItem


def check_slugs_uniqueness(structure: List["FormStructureItem"]) -> List["FormStructureItem"]:
    slugs: set[str] = set()
    for field in structure:
        assert field.slug not in slugs, "Structure fields should contain unique slugs."
        slugs.add(field.slug)

    return structure


def check_labels_uniqueness(structure: List["FormStructureItem"]) -> List["FormStructureItem"]:
    labels: set[str] = set()
    for field in structure:
        assert field.label not in labels, "Structure fields should contain unique labels."
        labels.add(field.label)
    return structure


def check_fields_count(structure: List["FormStructureItem"]) -> List["FormStructureItem"]:
    assert len(structure) > 0, "Form structure should contain at least one field."
    return structure
