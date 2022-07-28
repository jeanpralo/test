"""create initial tables

Revision ID: 23006aa6f75a
Revises: 
Create Date: 2022-07-27 14:33:41.918845

"""
import uuid

from alembic import op
import sqlalchemy as sa
import sqlalchemy.sql.functions as safunc

from faker import Faker
from faker.providers import DynamicProvider

fake = Faker()
job_status = DynamicProvider(
     provider_name="job_status",
     elements=["scheduled", "active", "invoicing", "to priced", "completed"],
)
fake.add_provider(job_status)


# revision identifiers, used by Alembic.
revision = '23006aa6f75a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    jobs = op.create_table(
        'jobs',
        sa.Column("job_id", sa.Text, primary_key=True, nullable=False),
        sa.Column("status", sa.Text, server_default="active"),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=safunc.current_timestamp()),
        sa.Column("contact_name", sa.Text),
        sa.Column("phone", sa.Text),
        sa.Column("description", sa.Text)

    )

    op.create_table(
        'notes',
        sa.Column("note_id", sa.Text, primary_key=True, nullable=False),
        sa.Column("job_id", sa.Text, nullable=False),
        sa.Column("data", sa.Text)
    )

    _jobs = []
    for _ in range(10):
        _jobs.append({
            'job_id': str(uuid.uuid4()),
            'status': fake.job_status(),
            'contact_name': fake.name(),
            'phone': fake.phone_number(),
            'description': fake.sentence(),
            'created_at': fake.past_datetime()
        })

    op.bulk_insert(
        jobs,
        _jobs
    )


def downgrade() -> None:
    op.drop_table('jobs')
    op.drop_table('notes')


