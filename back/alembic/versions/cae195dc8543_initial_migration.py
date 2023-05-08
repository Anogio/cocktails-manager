""" initial migration

Revision ID: cae195dc8543
Revises: 
Create Date: 2023-04-29 22:55:19.971252

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cae195dc8543"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cocktails",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, unique=True),
        sa.Column("method", sa.Text, nullable=False),
        sa.Column("family", sa.Text, nullable=False),
        sa.Column("addons", sa.ARRAY(sa.Text)),
        sa.Column("instructions", sa.Text),
    )

    op.create_table(
        "cocktail_doses",
        sa.Column(
            "cocktail_id",
            sa.Integer,
            sa.ForeignKey("cocktails.id"),
            primary_key=True,
            autoincrement=False,
        ),
        sa.Column("quantity_ounces", sa.Float, nullable=False),
        sa.Column("liquid", sa.Text, nullable=False, primary_key=True),
    )

    op.create_table(
        "cocktail_user_data",
        sa.Column(
            "cocktail_id",
            sa.Integer,
            sa.ForeignKey("cocktails.id"),
            primary_key=True,
            autoincrement=False,
        ),
        sa.Column("favorite_status", sa.Text),
        sa.Column("feedback", sa.Text),
    )


def downgrade() -> None:
    op.drop_table("cocktail_doses")
    op.drop_table("cocktail_user_data")
    op.drop_table("cocktails")
