# ============================================================
# 🎓 FastAPI Student Management System (CRUD) - SQLite Version
# ============================================================

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# ------------------------------------------------------------
# 🚀 Create FastAPI App
# ------------------------------------------------------------
app = FastAPI()

# ------------------------------------------------------------
# 🗄️ Database Configuration
# ------------------------------------------------------------
DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# ------------------------------------------------------------
# 🧱 Database Model (Table)
# ------------------------------------------------------------
class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    course = Column(String)

# Create table
Base.metadata.create_all(bind=engine)

# ------------------------------------------------------------
# 🧾 Pydantic Schema
# ------------------------------------------------------------
class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str

    class Config:
        from_attributes = True

# ------------------------------------------------------------
# 🔌 Dependency (DB Session)
# ------------------------------------------------------------
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# ------------------------------------------------------------
# 🏠 Home Route
# ------------------------------------------------------------
@app.get("/")
def home():
    return {"message": "Student Management System 🚀"}

# ------------------------------------------------------------
# ✅ 1. CREATE STUDENT
# ------------------------------------------------------------
@app.post("/students")
def create_student(student: Student, db: Session = Depends(get_db)):

    existing = db.query(StudentDB).filter(
        StudentDB.id == student.id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Student ID already exists"
        )

    new_student = StudentDB(
        id=student.id,
        name=student.name,
        age=student.age,
        course=student.course
    )

    db.add(new_student)

    db.commit()

    db.refresh(new_student)

    return {
        "message": "Student Added Successfully",
        "data": new_student
    }

# ------------------------------------------------------------
# ✅ 2. READ ALL STUDENTS
# ------------------------------------------------------------
@app.get("/students")
def get_all_students(db: Session = Depends(get_db)):

    students = db.query(StudentDB).all()

    return {
        "count": len(students),
        "data": students
    }

# ------------------------------------------------------------
# ✅ 3. READ SINGLE STUDENT
# ------------------------------------------------------------
@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

# ------------------------------------------------------------
# ✅ 4. UPDATE STUDENT
# ------------------------------------------------------------
@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    updated_student: Student,
    db: Session = Depends(get_db)
):

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = updated_student.name
    student.age = updated_student.age
    student.course = updated_student.course

    db.commit()

    db.refresh(student)

    return {
        "message": "Student Updated Successfully",
        "data": student
    }

# ------------------------------------------------------------
# ✅ 5. DELETE STUDENT
# ------------------------------------------------------------
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)

    db.commit()

    return {"message": "Student Deleted Successfully"}