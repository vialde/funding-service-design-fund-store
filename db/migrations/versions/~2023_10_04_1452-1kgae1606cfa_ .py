"""Add 'feedback_survey_config' column to round table

Revision ID: 1kgae1606cfa
Revises: a0a14c197848
Create Date: 2023-10-04 14:52:23.704133

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "1kgae1606cfa"
down_revision = "a0a14c197848"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("feedback_survey_config", sa.JSON(none_as_null=True), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("feedback_survey_config")

    # ### end Alembic commands ###
