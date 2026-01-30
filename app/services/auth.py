from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from app.models.auth import User, RefreshToken
from app.schemas.auth import UserCreate
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_refresh_token

class AuthService:
    def register_user(self, db: Session, user: UserCreate):
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(status_code=400, detail="Username already taken")
        
        hashed_password = hash_password(user.password)
        new_user = User(
            username=user.username,
            email=user.email,
            password_hash=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def authenticate_user(self, db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password_hash):
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        db.query(RefreshToken).filter(
            RefreshToken.user_id == user.id,
            or_(
                RefreshToken.revoked == True,
                RefreshToken.expires_at < datetime.utcnow()
            )
        ).delete(synchronize_session=False)

        db_refresh_token = RefreshToken(user_id=user.id, token=refresh_token)
        db.add(db_refresh_token)
        db.commit()
        
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh_access_token(self, db: Session, token_str: str):
        token_in_db = db.query(RefreshToken).filter_by(token=token_str).first()
        if not token_in_db:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        if not token_in_db or token_in_db.revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

        try:
            payload = decode_refresh_token(token_str)
            user_id = payload.get("sub")
        except Exception:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
        
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        new_access_token = create_access_token({"sub": str(user.id)})
        new_refresh_token = create_refresh_token({"sub": str(user.id)})
        
        token_in_db.token = new_refresh_token
        db.commit()
        
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}

    def logout(self, db: Session, token_str: str):
        token_in_db = db.query(RefreshToken).filter_by(token=token_str).first()
        if token_in_db:
            token_in_db.revoked = True
            db.commit()
        return {"message": "Logged out successfully"}
