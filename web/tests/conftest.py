"""
Test fixtures for the Paleo-Analysis backend.

In-memory SQLite + FastAPI dependency override so tests run hermetically
without touching the real paleo.db file.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture()
def test_engine():
    """Fresh in-memory SQLite engine per test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # share the single in-memory connection across sessions
    )
    return engine


@pytest.fixture()
def TestSession(test_engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture()
def app(test_engine, TestSession):
    """
    Build the FastAPI app with a test engine wired in.

    Importing main triggers the router imports, which pull in models; the
    models register themselves against db.base.Base. We then create tables on
    the test engine (not the real one in db.session).
    """
    from db.base import Base
    from main import app as fastapi_app
    from api.deps import get_db
    import models  # noqa: F401  # ensure all models are registered on Base

    Base.metadata.create_all(bind=test_engine)

    def _override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    fastapi_app.dependency_overrides[get_db] = _override_get_db
    yield fastapi_app
    fastapi_app.dependency_overrides.clear()


@pytest.fixture()
def client(app):
    return TestClient(app)


@pytest.fixture()
def db(TestSession):
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


# ---------------------------------------------------------------------------
# Seed helpers
# ---------------------------------------------------------------------------

@pytest.fixture()
def seed_genus(app, db):
    from models.genus import Genus

    g = Genus(
        id=1,
        Genus="Tyrannosaurus",
        Family="Tyrannosauridae",
        Infraorder="Coelurosauria",
        Suborder="Theropoda",
        Order="Saurischia",
        Informal=False,
        TaxonSize=12,
        Diet="Carnivore",
        MaxMYA=68.0,
        MinMYA=66.0,
        LifespanMYA=2.0,
        EarlyAge="Maastrichtian",
        LateAge="Maastrichtian",
        EarlyPeriod="Cretaceous",
        LatePeriod="Cretaceous",
    )
    db.add(g)
    db.commit()
    db.refresh(g)
    return g


@pytest.fixture()
def seed_species(app, db, seed_genus):
    from models.species import Species

    s = Species(
        id=1,
        Species="Tyrannosaurus rex",
        Genus="Tyrannosaurus",
        Diet="Carnivore",
        MaxMYA=68,
        MinMYA=66,
        LifespanMYA=2.0,
        EarlyAge="Maastrichtian",
        LateAge="Maastrichtian",
        EarlyPeriod="Cretaceous",
        LatePeriod="Cretaceous",
        genus_id=seed_genus.id,
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@pytest.fixture()
def seed_fossil(app, db, seed_genus):
    from models.fossil import Fossil

    f = Fossil(
        id=1,
        Fossil="Tyrannosaurus rex",
        Longitude=-106.5,
        Latitude=47.1,
        Formation="Hell Creek",
        Country="USA",
        State="Montana",
        County="Garfield",
        Collection=1,
        GeoComments="none",
        PaleoLongitude=-80.0,
        PaleoLatitude=52.0,
        GeoPlate="NAM",
        GeoGroup="Montana Group",
        Member="Upper",
        PaleoModel="Scotese",
        genus_id=seed_genus.id,
    )
    db.add(f)
    db.commit()
    db.refresh(f)
    return f
