"""structure

Revision ID: 600f8a7729b7
Revises: a50edf75721d
Create Date: 2024-08-20 07:56:45.424670

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "600f8a7729b7"
down_revision: Union[str, None] = "a50edf75721d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("forms", sa.Column("structure", sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("forms", "structure")
    # ### end Alembic commands ###
