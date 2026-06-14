from .core.config import settings
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.router.knights import knights_router
from app.router.auth import auth_router
from app.router.ravens import ravens_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("The Red Keep is open!")
    yield
    print("The Red Keep is closed!")

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
app.include_router(knights_router)
app.include_router(ravens_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"status": "The realm is secure."}