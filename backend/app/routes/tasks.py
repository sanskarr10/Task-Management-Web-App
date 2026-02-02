from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Task, User
from app.schemas import TaskCreate
from app.dependencies import get_current_user

router = APIRouter(prefix="/tasks")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_tasks(email=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    return db.query(Task).filter(Task.user_id == user.id).all()

@router.post("/")
def create_task(task: TaskCreate, email=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    new_task = Task(
        title=task.title,
        user_id=user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    t = db.query(Task).get(task_id)
    db.delete(t)
    db.commit()
    return {"deleted": True}
