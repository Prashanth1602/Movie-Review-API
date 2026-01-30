from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.auth import User
from app.core.security import hash_password
import logging

logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
    if not user:
        logger.info(f"Creating first superuser: {settings.FIRST_SUPERUSER}")
        user = User(
            email=settings.FIRST_SUPERUSER,
            username=settings.FIRST_SUPERUSER.split("@")[0], 
            password_hash=hash_password(settings.FIRST_SUPERUSER_PASSWORD),
            role="admin",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        logger.info("First superuser already exists.")
