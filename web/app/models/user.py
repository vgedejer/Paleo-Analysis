from sqlalchemy import Boolean, Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.sql import expression
from db.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        # A user is uniquely identified by (provider, provider's subject id).
        # Enforced now so OAuth account-linking can't create duplicates later.
        UniqueConstraint("auth_provider", "auth_subject", name="uq_users_auth_identity"),
    )

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    favorite_dino = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    middle_initial = Column(String, index=True, nullable=True)

    # OAuth identity — populated once OAuth lands (e.g. provider="google" and
    # subject = the provider's stable user id, or a Supabase auth uid). Nullable
    # so accounts created before a provider is linked stay valid. No auth logic
    # is implemented yet; these columns just make the schema OAuth-ready.
    auth_provider = Column(String, index=True, nullable=True)
    auth_subject = Column(String, index=True, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default=expression.true())

    created_on = Column(DateTime, index=True)
    last_modified = Column(DateTime, index=True)
