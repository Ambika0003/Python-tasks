# ============================================================
# 📝 FastAPI TODO App (CRUD) - MySQL Version
# pip install fastapi uvicorn sqlalchemy pymysql
# ============================================================

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ------------------------------------------------------------
# 🚀 App
# ------------------------------------------------------------
app = FastAPI()

# ------------------------------------------------------------
# 🗄️ MySQL Configuration
# ------------------------------------------------------------
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/todo_db"

'''
mysql+pymysql://root:1234@localhost:3306/todo_db
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
class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    completed = Column(Boolean, default=False)

# Create table
Base.metadata.create_all(bind=engine)

# ------------------------------------------------------------
# 🧾 Schema (Pydantic)
# ------------------------------------------------------------
class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

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
    return {"message": "FastAPI + MySQL TODO 🚀"}

# ------------------------------------------------------------
# ✅ CREATE
# ------------------------------------------------------------
@app.post("/todos")
def create_todo(todo: Todo, db: Session = Depends(get_db)):
    existing = db.query(TodoDB).filter(TodoDB.id == todo.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="ID already exists")

    new_todo = TodoDB(
        id=todo.id,
        title=todo.title,
        completed=todo.completed
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return {"message": "Created", "data": new_todo}

# ------------------------------------------------------------
# ✅ READ ALL
# ------------------------------------------------------------
@app.get("/todos")
def get_all(db: Session = Depends(get_db)):
    todos = db.query(TodoDB).all()
    return {"count": len(todos), "data": todos}

# ------------------------------------------------------------
# ✅ READ ONE
# ------------------------------------------------------------
@app.get("/todos/{todo_id}")
def get_one(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Not found")

    return todo

# ------------------------------------------------------------
# ✅ UPDATE
# ------------------------------------------------------------
@app.put("/todos/{todo_id}")
def update(todo_id: int, updated: Todo, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Not found")

    todo.title = updated.title
    todo.completed = updated.completed

    db.commit()
    db.refresh(todo)

    return {"message": "Updated", "data": todo}

# ------------------------------------------------------------
# ✅ DELETE
# ------------------------------------------------------------
@app.delete("/todos/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(todo)
    db.commit()

    return {"message": "Deleted"}
