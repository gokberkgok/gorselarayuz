"""
Pydantic schemas for request validation and response serialization.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, time, datetime


# ── Auth ────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
    name: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Types ───────────────────────────────────────────────
class TypeCreate(BaseModel):
    name: str


class TypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# ── Places ──────────────────────────────────────────────
class PlaceCreate(BaseModel):
    name: str
    type_id: int
    description: Optional[str] = ""
    image_url: Optional[str] = ""


class PlaceUpdate(BaseModel):
    name: Optional[str] = None
    type_id: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class PlaceResponse(BaseModel):
    id: int
    name: str
    type_id: int
    type_name: Optional[str] = None
    description: str
    image_url: str
    is_active: bool
    created_by: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Reservations ────────────────────────────────────────
class ReservationCreate(BaseModel):
    place_id: int
    date: date
    start_time: time
    end_time: time


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    user_name: Optional[str] = None
    place_id: int
    place_name: Optional[str] = None
    date: date
    start_time: time
    end_time: time
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Stats ───────────────────────────────────────────────
class DashboardStats(BaseModel):
    total_users: int
    total_places: int
    total_reservations: int
    pending_reservations: int
    approved_reservations: int
