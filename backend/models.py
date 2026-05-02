"""
SQLAlchemy ORM models for the reservation system.
"""
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Date, Time,
    ForeignKey, DateTime, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from backend.database import Base


# ── Enums ───────────────────────────────────────────────
class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"


class ReservationStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    cancelled = "cancelled"
    rejected = "rejected"


# ── Users ───────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.user, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    places = relationship("Place", back_populates="creator")
    reservations = relationship("Reservation", back_populates="user")


# ── Types ───────────────────────────────────────────────
class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    places = relationship("Place", back_populates="type_rel")


# ── Places ──────────────────────────────────────────────
class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    type_id = Column(Integer, ForeignKey("types.id"), nullable=False)
    description = Column(Text, default="")
    image_url = Column(String(500), default="")
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    type_rel = relationship("Type", back_populates="places")
    creator = relationship("User", back_populates="places")
    reservations = relationship("Reservation", back_populates="place")


# ── Reservations ────────────────────────────────────────
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(
        SAEnum(ReservationStatus),
        default=ReservationStatus.pending,
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="reservations")
    place = relationship("Place", back_populates="reservations")
