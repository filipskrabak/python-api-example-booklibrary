from sqlalchemy import Date, DateTime, Enum, Integer, String, ForeignKey
import enum
from sqlalchemy.sql.schema import Column
from dbs_assignment.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

# ENUMS
class CardStatus(enum.Enum):
    active = 'active'
    inactive = 'inactive'
    expired = 'expired'

class InstanceStatus(enum.Enum):
    available = 'available'
    reserved = 'reserved'

class InstanceType(enum.Enum):
    physical = 'physical'
    ebook = 'ebook'
    audiobook = 'audiobook'

class RentalStatus(enum.Enum):
    active = 'active'
    overdue = 'overdue'
    returned = 'returned'

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    identification_num = Column(String, unique=True, nullable=False)
    email = Column(String(254), unique=True, nullable=True)
    name = Column(String)
    surname = Column(String)
    birth_date = Column(Date)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

    rentals = relationship("Rental", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")

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

    authors = relationship("Author", secondary="publication_authors", back_populates="publications")
    categories = relationship("Category", secondary="publication_categories", back_populates="publications")

class Author(Base):
    __tablename__ = "authors"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

    publications = relationship("Publication", secondary="publication_authors", back_populates="authors")

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

    publications = relationship("Publication", secondary="publication_categories", back_populates="categories")

class PublicationAuthor(Base):
    __tablename__ = "publication_authors"

    publication_id = Column(UUID(as_uuid=True), ForeignKey("publications.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True, nullable=False)

class PublicationCategory(Base):
    __tablename__ = "publication_categories"

    publication_id = Column(UUID(as_uuid=True), ForeignKey("publications.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True, nullable=False)

class Instance(Base):
    __tablename__ = "instances"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    type = Column(Enum(InstanceType), nullable=False)
    publisher = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(Enum(InstanceStatus), nullable=False)
    publication_id = Column(UUID(as_uuid=True), ForeignKey("publications.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

    publication = relationship("Publication", backref=backref("instances", cascade="all, delete"))

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    instance_id = Column(UUID(as_uuid=True), ForeignKey("instances.id", ondelete="CASCADE"), nullable=False)
    duration = Column(Integer, nullable=False)
    status = Column(Enum(RentalStatus), nullable=False)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="rentals")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    publication_id = Column(UUID(as_uuid=True), ForeignKey("publications.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True))
    expire_at = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="reservations")
