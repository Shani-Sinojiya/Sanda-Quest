from fastapi import FastAPI
from app.routes import router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

list = [
    "*",
    "http://localhost:8000",
    "https://localhost:8000",
    "http://localhost:8001",
    "https://localhost:8001",
    "http://localhost:8081",
    "https://localhost:8081",
]

app = FastAPI(title="SandalQuest API", version="0.0.1",
              description="API for SandalQuest project")

app.add_middleware(
    CORSMiddleware,
    allow_origins=list,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)

# Mounting static files url: /static/outputs
app.mount("/static/outputs",
          StaticFiles(directory="app/static/outputs"), name="outputs")


@app.get("/")
def read_root():
    return {"message": "Welcome to SandalQuest API"}
