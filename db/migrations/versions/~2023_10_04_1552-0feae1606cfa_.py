"""Migrate data from 'requires_feedback' to 'feedback_survey_config' column

Revision ID: 0feae1606cfa
Revises: 1kgae1606cfa
Create Date: 2023-10-04 15:52:23.704133

"""
import json

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "0feae1606cfa"
down_revision = "1kgae1606cfa"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # migrate the data from 'requires_feedback' to 'feedback_survey_config' column
    connection = op.get_bind()
    query = sa.text("SELECT id, requires_feedback, feedback_survey_config FROM round")
    rounds = connection.execute(query)
    for id, requires_feedback, feedback_survey_config in rounds:
        if feedback_survey_config is not None:
            new_feedback_survey_config = feedback_survey_config
        else:
            new_feedback_survey_config = {}
        new_feedback_survey_config["requires_section_feedback"] = requires_feedback
        if requires_feedback is True:
            new_feedback_survey_config["requires_survey"] = True
            new_feedback_survey_config["isSurveyOptional"] = False
        else:
            new_feedback_survey_config["requires_survey"] = False
            new_feedback_survey_config["isSurveyOptional"] = True

        new_feedback_survey_config = json.dumps(new_feedback_survey_config)
        update_query = sa.text(
            f"UPDATE round SET feedback_survey_config = '{new_feedback_survey_config}'"
            f" WHERE id = '{id}'"
        )
        connection.execute(update_query)

    # drop the 'requires_feedback' column
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("requires_feedback")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # migrate the data from 'feedback_survey_config' to 'requires_feedback' column
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("requires_feedback", sa.Boolean(), nullable=True))

    connection = op.get_bind()
    query = sa.text("SELECT id, requires_feedback, feedback_survey_config FROM round")
    rounds = connection.execute(query)
    for id, requires_feedback, feedback_survey_config in rounds:
        if feedback_survey_config is not None:
            requires_feedback = feedback_survey_config.get(
                "requires_section_feedback", False
            )
        else:
            requires_feedback = False
        new_requires_feedback = json.dumps(requires_feedback)
        update_query = sa.text(
            f"UPDATE round SET requires_feedback = '{new_requires_feedback}' WHERE id ="
            f" '{id}'"
        )
        connection.execute(update_query)

    # ### end Alembic commands ###
