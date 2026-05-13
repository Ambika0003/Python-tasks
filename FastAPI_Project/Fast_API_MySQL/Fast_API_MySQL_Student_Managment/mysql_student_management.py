# ============================================================
# 🎓 FastAPI Student Management System (CRUD) - MySQL Version
# pip install fastapi uvicorn sqlalchemy pymysql
# ============================================================

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ------------------------------------------------------------
# 🚀 App
# ------------------------------------------------------------
app = FastAPI()

# ------------------------------------------------------------
# 🗄️ MySQL Configuration
# ------------------------------------------------------------
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/student_db"

'''
mysql+pymysql://root:1234@localhost:3306/student_db
│      │         │    │    │         │    │
│      │         │    │    │         │    └── Database name
│      │         │    │    │         └────── Port
│      │         │    │    └──────────────── Hostname
│      │         │    └───────────────────── Password
│      │         └────────────────────────── Username
│      └──────────────────────────────────── Driver
└─────────────────────────────────────────── Database type
'''

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# ------------------------------------------------------------
# 🧱 Table Model
# ------------------------------------------------------------
class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    age = Column(Integer)
    course = Column(String(255))

# Create table
Base.metadata.create_all(bind=engine)

# ------------------------------------------------------------
# 🧾 Schema (Pydantic)
# ------------------------------------------------------------
class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str

    class Config:
        orm_mode = True

# ------------------------------------------------------------
# 🔌 DB Dependency
# ------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------------------------------------
# 🏠 Home
# ------------------------------------------------------------
@app.get("/")
def home():
    return {"message": "FastAPI + MySQL Student Management 🚀"}

# ------------------------------------------------------------
# ✅ CREATE
# ------------------------------------------------------------
@app.post("/students")
def create_student(student: Student, db: Session = Depends(get_db)):
    existing = db.query(StudentDB).filter(StudentDB.id == student.id).first()

    if existing:
        raise HTTPException(status_code=400, detail="ID already exists")

    new_student = StudentDB(
        id=student.id,
        name=student.name,
        age=student.age,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {"message": "Student Created", "data": new_student}

# ------------------------------------------------------------
# ✅ READ ALL
# ------------------------------------------------------------
@app.get("/students")
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(StudentDB).all()

    return {
        "count": len(students),
        "data": students
    }

# ------------------------------------------------------------
# ✅ READ ONE
# ------------------------------------------------------------
@app.get("/students/{student_id}")
def get_one_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student

# ------------------------------------------------------------
# ✅ UPDATE
# ------------------------------------------------------------
@app.put("/students/{student_id}")
def update_student(student_id: int, updated: Student, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = updated.name
    student.age = updated.age
    student.course = updated.course

    db.commit()
    db.refresh(student)

    return {"message": "Student Updated", "data": student}

# ------------------------------------------------------------
# ✅ DELETE
# ------------------------------------------------------------
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"message": "Student Deleted"}