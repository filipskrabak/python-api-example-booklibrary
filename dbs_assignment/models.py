from sqlalchemy import Date, DateTime, Enum, Integer, String, ForeignKey
import enum
from sqlalchemy.sql.schema import Column
from dbs_assignment.database import Base
from sqlalchemy.dialects.postgresql import UUID

# ENUMS
class CardStatus(enum.Enum):
    active = 'active'
    inactive = 'inactive'
    expired = 'expired'

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

class Card(Base):
    __tablename__ = "cards"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    magstripe = Column(String(20), nullable=False)
    status = Column(Enum(CardStatus), nullable=False)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

class Publication(Base):
    __tablename__ = "publications"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
