# myapp/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# from backend.auth import models, routes
from backend.auth import routes as auth_routes, models as auth_models
from backend.proj import routes as proj_routes, models as proj_models
from backend.database import engine, Base

import os

# create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# includ auth routes
app.include_router(auth_routes.router, prefix="/api/v1", tags=["auth"])
app.include_router(proj_routes.router, prefix="/api/v1", tags=["projects"])


# Optional API route
@app.get("/api/v1/hello")
def read_data():
    return {"msg": "Hello from backend!"}

# Serve static files
frontend_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
