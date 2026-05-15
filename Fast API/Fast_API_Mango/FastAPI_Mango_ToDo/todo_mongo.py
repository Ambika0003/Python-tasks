# ============================================================
# 📝 FastAPI TODO App - MongoDB Atlas + MongoEngine
# pip install fastapi uvicorn mongoengine pymongo
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mongoengine import connect, Document, IntField, StringField, BooleanField

# ------------------------------------------------------------
# 🚀 FastAPI App
# ------------------------------------------------------------
app = FastAPI()

# ------------------------------------------------------------
# 🌐 MongoDB Atlas Connection
# ------------------------------------------------------------
MONGO_URL = "mongodb+srv://smambika869_db_user:I7n2zwZWtnkw9ZpU@ambika.obcayra.mongodb.net/todo_db?retryWrites=true&w=majority"
'''
mongodb+srv://username:password@clustername.xxxxx.mongodb.net/todo_db?retryWrites=true&w=majority
│              │        │        │                              │
│              │        │        │                              └── Database name
│              │        │        └──────────────────────────────── Cluster URL
│              │        └───────────────────────────────────────── Password
│              └────────────────────────────────────────────────── Username
└───────────────────────────────────────────────────────────────── MongoDB protocol
'''
connect(host=MONGO_URL)

# ------------------------------------------------------------
# 🧱 MongoDB Model (Like SQLAlchemy Model)
# ------------------------------------------------------------
class TodoDB(Document):
    id = IntField(primary_key=True)
    title = StringField(required=True)
    completed = BooleanField(default=False)

    meta = {
        "collection": "todos"
    }

# ------------------------------------------------------------
# 🧾 Pydantic Schema
# ------------------------------------------------------------
class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

# ------------------------------------------------------------
# 🏠 Home Route
# ------------------------------------------------------------
@app.get("/")
def home():
    return {"message": "FastAPI + MongoDB Atlas 🚀"}

# ------------------------------------------------------------
# ✅ 1. CREATE TODO
# ------------------------------------------------------------
@app.post("/todos")
def create_todo(todo: Todo):

    # Check duplicate ID
    existing = TodoDB.objects(id=todo.id).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="ID already exists"
        )

    new_todo = TodoDB(
        id=todo.id,
        title=todo.title,
        completed=todo.completed
    )

    new_todo.save()

    return {
        "message": "Todo created",
        "data": todo
    }

# ------------------------------------------------------------
# ✅ 2. READ ALL TODOS
# ------------------------------------------------------------
@app.get("/todos")
def get_all_todos():

    todos = TodoDB.objects()

    data = []

    for todo in todos:
        data.append({
            "id": todo.id,
            "title": todo.title,
            "completed": todo.completed
        })

    return {
        "count": len(data),
        "data": data
    }

# ------------------------------------------------------------
# ✅ 3. READ SINGLE TODO
# ------------------------------------------------------------
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):

    todo = TodoDB.objects(id=todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return {
        "id": todo.id,
        "title": todo.title,
        "completed": todo.completed
    }

# ------------------------------------------------------------
# ✅ 4. UPDATE TODO
# ------------------------------------------------------------
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated: Todo):

    todo = TodoDB.objects(id=todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    todo.title = updated.title
    todo.completed = updated.completed

    todo.save()

    return {
        "message": "Todo updated successfully"
    }

# ------------------------------------------------------------
# ✅ 5. DELETE TODO
# ------------------------------------------------------------
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):

    todo = TodoDB.objects(id=todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    todo.delete()

    return {
        "message": "Todo deleted successfully"
    }
