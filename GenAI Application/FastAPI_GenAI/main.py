from fastapi import FastAPI
from routes import router

app = FastAPI()

# Register Routes
app.include_router(router)