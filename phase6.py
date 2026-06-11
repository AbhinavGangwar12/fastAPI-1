from contextlib import asynccontextmanager
from fastapi import FastAPI , APIRouter
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Ravens dispatched: The realm is notified.")
    yield
    print("The Maesters have recorded the events: The realm is at peace.")

app = FastAPI(title="The Hedge knight")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

tourney_router = APIRouter(prefix="/tourneys", tags=["Tournaments"])
@tourney_router.get("/")
async def get_tourneys():
    return {"message": "Welcome to the Ashford Tourney!"}

app.include_router(tourney_router)