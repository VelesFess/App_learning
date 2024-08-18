"""Zero migration admin

Revision ID: 6a92ce40082a
Revises: 6030674d69ab
Create Date: 2024-08-17 16:47:03.344043

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6a92ce40082a"
down_revision: Union[str, None] = "6030674d69ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO user_list (login, name, password, email)
        VALUES ('admin', 'admin', '$2a$12$XWpRLWarZnJrg7VCJ1bkgO6jqqT4CPluOGjk5kLf6iqLnsj/Jp7jS', 'admin@example.com')
    """
    )


def downgrade() -> None:
    pass
