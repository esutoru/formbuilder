"""fill_form_structure

Revision ID: f9e57b4441c0
Revises: 600f8a7729b7
Create Date: 2024-09-04 07:48:05.823797

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import MetaData, Table, orm, update

STRUCTURE: list = [
    {
        "slug": "title",
        "label": "Title",
        "category": "text",
        "params": {
            "required": True,
            "help_text": "",
            "default_value": "",
            "min_length": 3,
            "max_length": 20,
        },
    }
]


# revision identifiers, used by Alembic.
revision: str = "f9e57b4441c0"
down_revision: Union[str, None] = "600f8a7729b7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    form_table = Table("forms", MetaData(), autoload_with=bind)

    session.execute(update(form_table).values(structure=STRUCTURE))
    session.commit()


def downgrade() -> None:
    pass
