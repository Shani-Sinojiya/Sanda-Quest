from fastapi import FastAPI
from app.routes import router
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="SandalQuest API", version="0.0.1",
              description="API for SandalQuest project")
app.include_router(router)

app.mount("/static/outputs",
          StaticFiles(directory="app/static/outputs"), name="outputs")


@app.get("/")
def read_root():
    return {"message": "Welcome to SandalQuest API"}
