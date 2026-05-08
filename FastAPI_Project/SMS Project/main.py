#��Step 1: Import Libraries 
from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel 
from typing import List 

#�Step 2: Create App 
app = FastAPI()

#��Step 3: Create Data Model (Schema) 
class Student(BaseModel): 
    id: int 
    name: str 
    age : int
    course : str
    marks : int

#��Step 4: Temporary Database
students=[]

#Step:5 Create FastAPI Application 
@app.get("/") 
def home(): 
    return {"message": "Student Management system Data"} 

#Step 6:  Create API – Add Student 
@app.post("/students") 
def create_student(student: Student): 
     
    for s in students:
        if s.id == student.id:
            raise HTTPException(status_code=400, detail="Student ID already exists")

    students.append(student)

    return {
        "message": "Student Added Successfully",
        "data": student
    }

# Step 7: Create API – Get All Students 
@app.get("/students") 
def get_student(): 
    return students

#Step 8 : Create API – Get Student By ID 
@app.get("/students/{student_id}")
def get_student(student_id: int): 
    for student in students: 
        if student.id == student_id: 
            return student 
    raise HTTPException(status_code=404, detail="Student Data Not Found") 

#Step 9: Create API – Update Student 
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student): 
    for index, student in enumerate(students): 
        if students[index].id == student_id: 
            students[index] = updated_student
            return {"message": "Student Data Updated successfully", "data": 
updated_student} 
    raise HTTPException(status_code=404, detail="Student Data Not Found") 

#Step 10 : Create API – Delete Student 
@app.delete("/students/{student_id}") 
def delete_student(student_id: int): 
    for index, student in enumerate(students): 
        if student.id == student_id: 
            deleted = students.pop(index) 
            return {"message": "Student Data Deleted successfully", "data": 
deleted} 
    raise HTTPException(status_code=404, detail="Student Data Not Found") 
