from sqlalchemy import Date, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql.schema import Column
from dbs_assignment.database import Base
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    identification_num = Column(String(10), unique=True, nullable=False)
    email = Column(String(254), unique=True, nullable=True)
    name = Column(String)
    surname = Column(String)
    birth_date = Column(Date)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

