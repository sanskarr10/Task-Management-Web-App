from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.dependencies import get_current_user

router = APIRouter(prefix="/profile")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def profile(email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    return {"email": user.email}
