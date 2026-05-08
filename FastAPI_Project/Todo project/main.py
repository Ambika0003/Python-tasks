#��Step 1: Import Libraries
from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel 
from typing import List 

#�Step 2: Create App 
app = FastAPI() 

#Step 3: Create Data Model (Schema) 
class Todo(BaseModel): 
    id: int 
    title: str 
    completed: bool = False

#Step 4: Temporary Database 
todos = [] 

#🔹CRUD OPERATIONS

#✅1. Create Todo (POST)
@app.post("/todos") 
def create_todo(todo: Todo): 
    todos.append(todo) 
    return {"message": "Todo added", "data": todo} 

#✅2. Read All Todos (GET) 
@app.get("/todos") 
def get_todos(): 
    return todos 

#✅3. Read Single Todo (GET by ID) 
@app.get("/todos/{todo_id}") 
def get_todo(todo_id: int): 
    for todo in todos: 
        if todo.id == todo_id: 
            return todo 
    raise HTTPException(status_code=404, detail="Todo not found") 

#✅4. Update Todo (PUT)
@app.put("/todos/{todo_id}") 
def update_todo(todo_id: int, updated_todo: Todo): 
    for index, todo in enumerate(todos): 
        if todo.id == todo_id: 
            todos[index] = updated_todo 
            return {"message": "Updated successfully", "data": 
updated_todo} 
    raise HTTPException(status_code=404, detail="Todo not found")

#✅5. Delete Todo (DELETE) 
@app.delete("/todos/{todo_id}") 
def delete_todo(todo_id: int): 
    for index, todo in enumerate(todos): 
        if todo.id == todo_id: 
            deleted = todos.pop(index) 
            return {"message": "Deleted successfully", "data": 
deleted} 
    raise HTTPException(status_code=404, detail="Todo not found") 

