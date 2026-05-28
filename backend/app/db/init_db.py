from app.core.config import get_settings
from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.user import User
from app.seed.seed_loader import load_seed


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        settings = get_settings()
        admin = (
            db.query(User).filter(User.username == settings.admin_username).first()
        )
        if not admin:
            admin = User(
                username=settings.admin_username,
                password_hash=hash_password(settings.admin_password),
                role="admin",
            )
            db.add(admin)
            db.commit()
        load_seed(db, replace=False)
    finally:
        db.close()
