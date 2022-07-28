from sqlalchemy import Column, BigInteger, Text, TIMESTAMP
from fergus.db.models.base import BaseModel


class Notes(BaseModel):
    _table_description = "List of notes"

    __tablename__ = "notes"

    note_id = Column("note_id", Text, primary_key=True, nullable=False)
    job_id = Column("job_id", Text, nullable=False)
    data = Column("data", Text)

    def to_dict(self):
        return {
            "note_id": self.note_id,
            "data": self.data
        }
