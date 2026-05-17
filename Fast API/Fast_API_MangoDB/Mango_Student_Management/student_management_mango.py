# ============================================================
# 🎓 FastAPI Student Management System
# MongoDB Atlas + MongoEngine
# ============================================================

# Install Packages:
# pip install fastapi uvicorn mongoengine pymongo certifi

# Run Server:
# uvicorn student_management:app --reload

# Swagger UI:
# http://127.0.0.1:8000/docs

# ============================================================
# 📦 Imports
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mongoengine import (
    connect,
    Document,
    IntField,
    StringField,
    FloatField
)

import certifi

# ============================================================
# 🚀 FastAPI App
# ============================================================

app = FastAPI()

# ============================================================
# 🌐 MongoDB Atlas Connection
# ============================================================

MONGO_URL = "mongodb+srv://smambika869_db_user:I7n2zwZWtnkw9ZpU@ambika.obcayra.mongodb.net/student_management_db?retryWrites=true&w=majority"

connect(
    db="student_management",
    host=MONGO_URL,
    tls=True,
    tlsCAFile=certifi.where()
)

# ============================================================
# 🧱 MongoDB Model
# ============================================================

class StudentDB(Document):

    student_id = IntField(primary_key=True)

    name = StringField(required=True)

    age = IntField(required=True)

    course = StringField(required=True)

    marks = FloatField(required=True)

    meta = {
        "collection": "students"
    }

# ============================================================
# 🧾 Pydantic Schema
# ============================================================

class Student(BaseModel):

    student_id: int

    name: str

    age: int

    course: str

    marks: float

# ============================================================
# 🏠 Home Route
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Student Management System Working 🚀"
    }

# ============================================================
# ✅ 1. CREATE STUDENT
# ============================================================

@app.post("/students")
def create_student(student: Student):

    existing_student = StudentDB.objects(
        student_id=student.student_id
    ).first()

    if existing_student:

        raise HTTPException(
            status_code=400,
            detail="Student ID already exists"
        )

    new_student = StudentDB(

        student_id=student.student_id,
        name=student.name,
        age=student.age,
        course=student.course,
        marks=student.marks
    )

    new_student.save()

    return {

        "message": "Student added successfully",

        "data": student
    }

# ============================================================
# ✅ 2. READ ALL STUDENTS
# ============================================================

@app.get("/students")
def get_all_students():

    students = StudentDB.objects()

    data = []

    for student in students:

        data.append({

            "student_id": student.student_id,
            "name": student.name,
            "age": student.age,
            "course": student.course,
            "marks": student.marks
        })

    return {

        "count": len(data),

        "data": data
    }

# ============================================================
# ✅ 3. READ SINGLE STUDENT
# ============================================================

@app.get("/students/{student_id}")
def get_student(student_id: int):

    student = StudentDB.objects(
        student_id=student_id
    ).first()

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {

        "student_id": student.student_id,
        "name": student.name,
        "age": student.age,
        "course": student.course,
        "marks": student.marks
    }

# ============================================================
# ✅ 4. UPDATE STUDENT
# ============================================================

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    updated_student: Student
):

    student = StudentDB.objects(
        student_id=student_id
    ).first()

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = updated_student.name
    student.age = updated_student.age
    student.course = updated_student.course
    student.marks = updated_student.marks

    student.save()

    return {

        "message": "Student updated successfully"
    }

# ============================================================
# ✅ 5. DELETE STUDENT
# ============================================================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    student = StudentDB.objects(
        student_id=student_id
    ).first()

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.delete()

    return {

        "message": "Student deleted successfully"
    }