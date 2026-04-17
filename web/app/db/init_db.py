from db.base import Base
from db.session import engine


def init_db() -> None:
    # Import models so they register with Base.metadata before create_all.
    import models  # noqa: F401

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
