"""
FastAPI application entry point — includes routers, CORS, and seed data.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, Base, SessionLocal
from backend.models import User, Type, Place, UserRole
from backend.auth import hash_password, verify_password
from backend.routers import auth_router, places_router, reservations_router


def seed_database():
    """Populate the database with initial data on first run."""
    db = SessionLocal()
    try:
        # Seed admin user
        admin = db.query(User).filter(User.email == "admin@admin.com").first()
        if not admin:
            admin = User(
                name="Admin",
                email="admin@admin.com",
                password=hash_password("admin123"),
                role=UserRole.admin,
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("[OK] Seeded admin user: admin@admin.com / admin123")
        else:
            # Fix password if hash is invalid (e.g. imported from db.sql placeholder)
            try:
                if not verify_password("admin123", admin.password):
                    admin.password = hash_password("admin123")
                    db.commit()
                    print("[OK] Fixed admin password hash")
            except Exception:
                admin.password = hash_password("admin123")
                db.commit()
                print("[OK] Regenerated admin password hash")

        # Seed types
        type_names = ["Hotel", "Restaurant", "Room", "Cafe", "Spa"]
        existing_types = {t.name for t in db.query(Type).all()}
        for name in type_names:
            if name not in existing_types:
                db.add(Type(name=name))
        db.commit()
        print(f"[OK] Seeded types: {type_names}")

        # Seed sample places
        if db.query(Place).count() == 0:
            admin_user = db.query(User).filter(User.role == UserRole.admin).first()
            types = {t.name: t.id for t in db.query(Type).all()}

            sample_places = [
                # Hotels
                ("Grand Palace Hotel", "Hotel",
                 "Luxury 5-star hotel with panoramic city views, indoor pool, and world-class dining."),
                ("Seaside Resort & Spa", "Hotel",
                 "Beachfront resort offering premium suites, private beach access, and full spa services."),
                # Restaurants
                ("La Bella Cucina", "Restaurant",
                 "Authentic Italian fine dining with handmade pasta, wood-fired pizza, and curated wine list."),
                ("Sakura Sushi Bar", "Restaurant",
                 "Premium Japanese cuisine with fresh sashimi, omakase menu, and sake bar."),
                ("The Grill House", "Restaurant",
                 "Upscale steakhouse featuring dry-aged cuts, craft cocktails, and live jazz."),
                # Rooms
                ("Executive Meeting Room A", "Room",
                 "Modern meeting room for up to 20 people with projector, whiteboard, and video conferencing."),
                ("Creative Studio B", "Room",
                 "Bright co-working space with flexible seating, high-speed Wi-Fi, and coffee bar."),
                # Cafes
                ("Artisan Coffee Lab", "Cafe",
                 "Specialty coffee roastery with single-origin beans, pastries, and cozy reading nooks."),
                ("Garden Tea House", "Cafe",
                 "Tranquil tea house with over 50 premium teas, outdoor garden seating, and live acoustic music."),
                # Spa
                ("Serenity Wellness Center", "Spa",
                 "Full-service spa offering massage therapy, hot stone treatments, and aromatherapy sessions."),
            ]

            for name, type_name, desc in sample_places:
                place = Place(
                    name=name,
                    type_id=types[type_name],
                    description=desc,
                    created_by=admin_user.id,
                )
                db.add(place)
            db.commit()
            print(f"[OK] Seeded {len(sample_places)} sample places")

    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: create tables and seed data on startup."""
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield


# ── App setup ───────────────────────────────────────────
app = FastAPI(
    title="Reservation System API",
    description="A modern reservation system with role-based access control",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins for desktop app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router.router)
app.include_router(places_router.router)
app.include_router(reservations_router.router)


@app.get("/")
def root():
    return {"message": "Reservation System API is running", "version": "1.0.0"}
