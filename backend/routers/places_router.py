"""
Places router — CRUD for places and types.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from typing import Optional

from backend.database import get_db
from backend.models import Place, Type, User
from backend.schemas import (
    PlaceCreate, PlaceUpdate, PlaceResponse,
    TypeCreate, TypeResponse,
)
from backend.auth import get_current_user, require_admin

router = APIRouter(tags=["Places"])


# ── Types ───────────────────────────────────────────────
@router.get("/types", response_model=list[TypeResponse])
def list_types(db: Session = Depends(get_db)):
    """List all place types."""
    return db.query(Type).all()


@router.post("/types", response_model=TypeResponse, status_code=201)
def create_type(
    req: TypeCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new place type (admin only)."""
    existing = db.query(Type).filter(Type.name == req.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Type already exists")
    t = Type(name=req.name)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


# ── Places ──────────────────────────────────────────────
@router.get("/places", response_model=list[PlaceResponse])
def list_places(
    type_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List active places with optional filtering, search, and pagination."""
    q = db.query(Place).filter(Place.is_active == True)

    if type_id:
        q = q.filter(Place.type_id == type_id)

    if search:
        q = q.filter(Place.name.ilike(f"%{search}%"))

    places = q.offset(skip).limit(limit).all()

    result = []
    for p in places:
        resp = PlaceResponse(
            id=p.id,
            name=p.name,
            type_id=p.type_id,
            type_name=p.type_rel.name if p.type_rel else None,
            description=p.description,
            image_url=p.image_url,
            is_active=p.is_active,
            created_by=p.created_by,
            created_at=p.created_at,
        )
        result.append(resp)
    return result


@router.get("/places/random", response_model=list[PlaceResponse])
def random_places(
    count: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get random active places for the home page."""
    places = (
        db.query(Place)
        .filter(Place.is_active == True)
        .order_by(func.random())
        .limit(count)
        .all()
    )
    result = []
    for p in places:
        resp = PlaceResponse(
            id=p.id,
            name=p.name,
            type_id=p.type_id,
            type_name=p.type_rel.name if p.type_rel else None,
            description=p.description,
            image_url=p.image_url,
            is_active=p.is_active,
            created_by=p.created_by,
            created_at=p.created_at,
        )
        result.append(resp)
    return result


@router.get("/places/{place_id}", response_model=PlaceResponse)
def get_place(
    place_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a single place by ID."""
    p = db.query(Place).filter(Place.id == place_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Place not found")
    return PlaceResponse(
        id=p.id,
        name=p.name,
        type_id=p.type_id,
        type_name=p.type_rel.name if p.type_rel else None,
        description=p.description,
        image_url=p.image_url,
        is_active=p.is_active,
        created_by=p.created_by,
        created_at=p.created_at,
    )


@router.post("/places", response_model=PlaceResponse, status_code=201)
def create_place(
    req: PlaceCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new place (admin only)."""
    # Validate type exists
    type_obj = db.query(Type).filter(Type.id == req.type_id).first()
    if not type_obj:
        raise HTTPException(status_code=400, detail="Invalid type_id")

    place = Place(
        name=req.name,
        type_id=req.type_id,
        description=req.description or "",
        image_url=req.image_url or "",
        created_by=admin.id,
    )
    db.add(place)
    db.commit()
    db.refresh(place)

    return PlaceResponse(
        id=place.id,
        name=place.name,
        type_id=place.type_id,
        type_name=type_obj.name,
        description=place.description,
        image_url=place.image_url,
        is_active=place.is_active,
        created_by=place.created_by,
        created_at=place.created_at,
    )


@router.put("/places/{place_id}", response_model=PlaceResponse)
def update_place(
    place_id: int,
    req: PlaceUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update an existing place (admin only)."""
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    if req.name is not None:
        place.name = req.name
    if req.type_id is not None:
        type_obj = db.query(Type).filter(Type.id == req.type_id).first()
        if not type_obj:
            raise HTTPException(status_code=400, detail="Invalid type_id")
        place.type_id = req.type_id
    if req.description is not None:
        place.description = req.description
    if req.image_url is not None:
        place.image_url = req.image_url
    if req.is_active is not None:
        place.is_active = req.is_active

    db.commit()
    db.refresh(place)

    return PlaceResponse(
        id=place.id,
        name=place.name,
        type_id=place.type_id,
        type_name=place.type_rel.name if place.type_rel else None,
        description=place.description,
        image_url=place.image_url,
        is_active=place.is_active,
        created_by=place.created_by,
        created_at=place.created_at,
    )


@router.delete("/places/{place_id}")
def delete_place(
    place_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Soft-delete a place by deactivating it (admin only)."""
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    place.is_active = False
    db.commit()
    return {"detail": "Place deactivated"}
