from sqlalchemy import Column, BigInteger, Text, TIMESTAMP
from datetime import datetime as dt

from fergus.db.models.base import BaseModel


class Jobs(BaseModel):
    _table_description = "List of jobs"

    __tablename__ = "jobs"

    job_id = Column("job_id", Text, primary_key=True, nullable=False)
    status = Column("status", Text, default='active', nullable=False)
    created_at = Column("created_at", TIMESTAMP, nullable=False, default=dt.utcnow())
    contact_name = Column("contact_name", Text)
    phone = Column("phone", Text)
    description = Column("description", Text)

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "status": self.status,
            "created_at": self.created_at,
            "contact_name": self.contact_name,
            "phone": self.phone,
            "description": self.description
        }
