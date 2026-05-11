from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models  # noqa: F401  (register SQLAlchemy models before create_all)
from .db import Base, engine
from .routes import auth as auth_routes
from .routes import cargo as cargo_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intergalactic Cargo Portal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(cargo_routes.router)


@app.get("/health")
def health():
    return {"status": "ok"}
