"""
Reservations router — Create, cancel, approve, reject reservations.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional

from backend.database import get_db
from backend.models import Reservation, ReservationStatus, Place, User, UserRole
from backend.schemas import ReservationCreate, ReservationResponse, DashboardStats
from backend.auth import get_current_user, require_admin

router = APIRouter(prefix="/reservations", tags=["Reservations"])


def _to_response(r: Reservation) -> ReservationResponse:
    """Convert a Reservation ORM object to response schema."""
    return ReservationResponse(
        id=r.id,
        user_id=r.user_id,
        user_name=r.user.name if r.user else None,
        place_id=r.place_id,
        place_name=r.place.name if r.place else None,
        place_image_url=r.place.image_url if r.place else None,
        date=r.date,
        start_time=r.start_time,
        end_time=r.end_time,
        status=r.status.value,
        created_at=r.created_at,
    )


# ── User endpoints ─────────────────────────────────────
@router.post("", response_model=ReservationResponse, status_code=201)
def create_reservation(
    req: ReservationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new reservation (status = pending). Prevents double booking."""
    # Validate place exists and is active
    place = db.query(Place).filter(Place.id == req.place_id, Place.is_active == True).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found or inactive")

    # Validate time range
    if req.start_time >= req.end_time:
        raise HTTPException(status_code=400, detail="start_time must be before end_time")

    # Check for double booking — overlapping time on same place + date
    # Overlap condition: existing.start < new.end AND existing.end > new.start
    conflict = (
        db.query(Reservation)
        .filter(
            Reservation.place_id == req.place_id,
            Reservation.date == req.date,
            Reservation.status.in_([
                ReservationStatus.pending,
                ReservationStatus.approved,
            ]),
            Reservation.start_time < req.end_time,
            Reservation.end_time > req.start_time,
        )
        .first()
    )
    if conflict:
        raise HTTPException(
            status_code=409,
            detail="Time slot conflict: this place is already reserved for the selected time range",
        )

    reservation = Reservation(
        user_id=current_user.id,
        place_id=req.place_id,
        date=req.date,
        start_time=req.start_time,
        end_time=req.end_time,
        status=ReservationStatus.pending,
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return _to_response(reservation)


@router.get("/my", response_model=list[ReservationResponse])
def my_reservations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List current user's reservations."""
    reservations = (
        db.query(Reservation)
        .filter(Reservation.user_id == current_user.id)
        .order_by(Reservation.created_at.desc())
        .all()
    )
    return [_to_response(r) for r in reservations]


@router.put("/{reservation_id}/cancel", response_model=ReservationResponse)
def cancel_reservation(
    reservation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cancel own reservation."""
    reservation = (
        db.query(Reservation)
        .filter(Reservation.id == reservation_id, Reservation.user_id == current_user.id)
        .first()
    )
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if reservation.status == ReservationStatus.cancelled:
        raise HTTPException(status_code=400, detail="Already cancelled")

    reservation.status = ReservationStatus.cancelled
    db.commit()
    db.refresh(reservation)
    return _to_response(reservation)


# ── Admin endpoints ─────────────────────────────────────
@router.get("/all", response_model=list[ReservationResponse])
def all_reservations(
    status_filter: Optional[str] = Query(None),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """List all reservations (admin only), optionally filtered by status."""
    q = db.query(Reservation).order_by(Reservation.created_at.desc())
    if status_filter and status_filter in [s.value for s in ReservationStatus]:
        q = q.filter(Reservation.status == status_filter)
    return [_to_response(r) for r in q.all()]


@router.put("/{reservation_id}/approve", response_model=ReservationResponse)
def approve_reservation(
    reservation_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Approve a pending reservation (admin only)."""
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if reservation.status != ReservationStatus.pending:
        raise HTTPException(status_code=400, detail="Only pending reservations can be approved")

    reservation.status = ReservationStatus.approved
    db.commit()
    db.refresh(reservation)
    return _to_response(reservation)


@router.put("/{reservation_id}/reject", response_model=ReservationResponse)
def reject_reservation(
    reservation_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Reject a pending reservation (admin only)."""
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if reservation.status != ReservationStatus.pending:
        raise HTTPException(status_code=400, detail="Only pending reservations can be rejected")

    reservation.status = ReservationStatus.rejected
    db.commit()
    db.refresh(reservation)
    return _to_response(reservation)


@router.get("/stats", response_model=DashboardStats)
def dashboard_stats(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Return dashboard statistics (admin only)."""
    from backend.models import Type
    return DashboardStats(
        total_users=db.query(User).count(),
        total_places=db.query(Place).filter(Place.is_active == True).count(),
        total_reservations=db.query(Reservation).count(),
        pending_reservations=db.query(Reservation).filter(
            Reservation.status == ReservationStatus.pending
        ).count(),
        approved_reservations=db.query(Reservation).filter(
            Reservation.status == ReservationStatus.approved
        ).count(),
    )
