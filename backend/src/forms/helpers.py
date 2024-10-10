from backend.src.forms.structure.structure import FormStructure


def get_deleted_field_slugs(
    current_structure: FormStructure, new_stricture: FormStructure
) -> list[str]:
    current_slugs = [field.slug for field in current_structure]
    new_slugs = {field.slug for field in new_stricture}
    return [slug for slug in current_slugs if slug not in new_slugs]
