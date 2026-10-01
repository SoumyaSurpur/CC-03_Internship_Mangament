<<<<<<< HEAD
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker
import os

=======
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

>>>>>>> 01d1120c3fac282ed78a005fe358dd09e7350d03
engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///./applications.db"),
                       connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()
app = FastAPI(title="Application Service")

class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("student_id", "internship_id"),)
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False)
    internship_id = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="pending")

Base.metadata.create_all(engine)

class ApplyInput(BaseModel):
    student_id: int
    internship_id: int

class StatusInput(BaseModel):
    status: str

def out(x):
    return {"id": x.id, "student_id": x.student_id,
            "internship_id": x.internship_id, "status": x.status}

@app.get("/")
def home():
    return {"service": "application", "message": "running"}

@app.post("/applications")
def apply(data: ApplyInput):
    db = Session()
    try:
        existing = db.query(Application).filter_by(
            student_id=data.student_id, internship_id=data.internship_id).first()
        if existing: raise HTTPException(409, "Already applied to this internship")
        x = Application(student_id=data.student_id, internship_id=data.internship_id)
        db.add(x); db.commit(); db.refresh(x); return out(x)
    finally:
        db.close()

@app.get("/applications")
def list_all(student_id: int | None = None):
    db = Session()
    try:
        q = db.query(Application)
        if student_id is not None: q = q.filter_by(student_id=student_id)
        return [out(x) for x in q.order_by(Application.id).all()]
    finally:
        db.close()

@app.patch("/applications/{application_id}/status")
def update_status(application_id: int, data: StatusInput):
    if data.status not in {"pending", "accepted", "rejected"}:
        raise HTTPException(400, "Status must be pending, accepted, or rejected")
    db = Session()
    try:
        x = db.query(Application).filter_by(id=application_id).first()
        if not x: raise HTTPException(404, "Application not found")
        x.status = data.status; db.commit(); db.refresh(x); return out(x)
    finally:
        db.close()

@app.delete("/applications/{application_id}")
def delete(application_id: int):
    db = Session()
    try:
        x = db.query(Application).filter_by(id=application_id).first()
        if not x: raise HTTPException(404, "Application not found")
        db.delete(x); db.commit()
        return {"message": "Application deleted"}
    finally:
        db.close()
