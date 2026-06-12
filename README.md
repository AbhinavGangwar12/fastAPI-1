# 🚀 FastAPI Masterclass Guide

### A Complete Reference for Building Modern Python APIs

---

# 1. What is FastAPI?

**FastAPI** is a modern, high-performance web framework for building APIs with **Python 3.8+** based on standard Python type hints.

It is built on top of two powerful libraries:

* **Starlette** → Handles web routing and asynchronous capabilities.
* **Pydantic** → Handles data validation and serialization.

FastAPI combines speed, simplicity, and automatic documentation, making it one of the most popular backend frameworks in the Python ecosystem.

---

# 2. Why Use FastAPI?

## ⚡ Unmatched Speed

FastAPI is one of the fastest Python web frameworks available, offering performance comparable to frameworks built with:

* Node.js
* Go

This is possible because of its native asynchronous architecture.

---

## 🧑‍💻 Developer Productivity

By leveraging Python type hints, FastAPI provides:

* Smart autocompletion
* Better editor support
* Static type checking
* Early bug detection

This significantly improves development speed and code quality.

---

## 📚 Automatic Documentation

FastAPI automatically generates:

| Documentation Type | URL      |
| ------------------ | -------- |
| Swagger UI         | `/docs`  |
| ReDoc              | `/redoc` |

No manual API specification writing is required.

---

## ✅ Built-in Validation

FastAPI automatically validates incoming requests.

Example:

If an endpoint expects:

```python
age: int
```

and the client sends:

```json
{
  "age": "twenty"
}
```

FastAPI immediately returns:

```http
422 Unprocessable Entity
```

without requiring custom validation code.

---

# 🏰 Phase 1: Environment Setup & Tooling

## Definition

The foundation of a modern Python backend.

Environment setup ensures project dependencies remain isolated and do not conflict with other Python applications installed on your system.

---

## Tools Used

* WSL (Windows Subsystem for Linux)
* VS Code
* Python Virtual Environment (`venv`)

---

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate

# Install core libraries
pip install fastapi uvicorn pydantic sqlalchemy asyncpg alembic
```

---

# 🛣️ Phase 2: Routing & Parameters

## Definition

Routing determines how your API receives requests and sends responses.

---

## Concepts

### Path Parameters

Embedded directly inside the URL.

Example:

```text
/users/10
```

---

### Query Parameters

Appended after a question mark.

Example:

```text
/products?category=books
```

---

## Example

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.get("/squires/{squire_id}", status_code=status.HTTP_200_OK)
async def get_squire(squire_id: int):
    return {
        "squire_id": squire_id,
        "name": "Egg"
    }

@app.post("/tourneys", status_code=status.HTTP_201_CREATED)
async def enter_tourney(location: str, prize: int = 100):
    return {
        "message": f"Entered tourney at {location} for {prize} stags."
    }
```

---

# 🛡️ Phase 3: Core Mechanics & Pydantic v2

## Definition

Pydantic provides strict validation and serialization of data.

It guarantees that incoming and outgoing data follows a predefined structure.

---

## Creating Schemas

```python
from pydantic import BaseModel, Field

class HorseCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        description="The horse's name"
    )

    role: str = Field(
        ...,
        description="e.g., Destrier"
    )

class HorseResponse(HorseCreate):
    id: int
```

---

## Using Request & Response Models

```python
@app.post("/horses", response_model=HorseResponse)
async def add_horse(horse: HorseCreate):

    new_horse = horse.model_dump()

    return {
        "id": 1,
        **new_horse
    }
```

---

# 🔄 Phase 4: Dependency Injection

## Definition

Dependency Injection allows reusable logic to execute before an endpoint runs.

Common use cases:

* Authentication
* Authorization
* Database Sessions
* Shared Validation
* Logging

---

## Example

```python
from fastapi import Depends, HTTPException
from typing import Annotated

def check_knighthood(title: str = "Ser"):

    if title != "Ser":
        raise HTTPException(
            status_code=403,
            detail="Not a knight."
        )

    return title

KnightGuard = Annotated[
    str,
    Depends(check_knighthood)
]

@app.get("/armory")
async def enter_armory(title: KnightGuard):

    return {
        "message": f"Welcome, {title}."
    }
```

---

# 🗄️ Phase 5: Async Database Integration (SQLAlchemy 2.0)

## Definition

Persisting data in a PostgreSQL database using asynchronous operations.

Benefits:

* Non-blocking I/O
* Better scalability
* Improved performance under load

---

## Database Configuration

```python
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db"
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)
```

---

## Database Models

```python
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

class Base(DeclarativeBase):
    pass

class TourneyDB(Base):
    __tablename__ = "tourneys"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    location: Mapped[str]
```

---

## Database Dependency

```python
async def get_db():

    async with AsyncSessionLocal() as session:
        yield session
```

Usage:

```python
async def create_tourney(
    db: Annotated[
        AsyncSession,
        Depends(get_db)
    ]
):
    ...
```

---

# 🏗️ Phase 6: Architecture & Production

## Definition

Organizing large FastAPI applications into modular, maintainable components.

---

## Key Components

### APIRouter

Splits endpoints into separate modules.

### Lifespan Events

Handles startup and shutdown operations.

### CORS Middleware

Allows frontend applications to communicate with your backend.

---

## Example

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Startup: Opening gates.")

    yield

    print("Shutdown: Closing gates.")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)

tourney_router = APIRouter(
    prefix="/tourneys"
)

@tourney_router.get("/")
async def list_tourneys():
    return []

app.include_router(tourney_router)
```

---

# 🔐 Phase 7: Security & Authentication (JWT)

## Definition

Protecting API endpoints through authentication and authorization.

---

## Authentication Flow

```text
User Login
    ↓
Verify Credentials
    ↓
Generate JWT Token
    ↓
Return Token
    ↓
Client Stores Token
    ↓
Send Token with Requests
    ↓
Verify Token
    ↓
Grant Access
```

---

## Example

```python
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from typing import Annotated
import jwt

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)

async def get_current_knight(
    token: Annotated[
        str,
        Depends(oauth2_scheme)
    ]
):
    try:
        payload = jwt.decode(
            token,
            "SECRET_KEY",
            algorithms=["HS256"]
        )

        return payload.get("sub")

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
```

---

# 🦅 Phase 8: Background Tasks

## Definition

Run long-running tasks in the background while immediately returning a response to the client.

---

## Benefits

* Faster response times
* Better user experience
* Suitable for:

  * Sending emails
  * Notifications
  * File processing
  * Logging
  * Report generation

---

## Example

```python
from fastapi import (
    BackgroundTasks,
    status
)

import asyncio

async def send_raven(house: str):

    await asyncio.sleep(2)

    print(
        f"Message delivered to {house}"
    )

@app.post(
    "/messages",
    status_code=status.HTTP_202_ACCEPTED
)
async def dispatch(
    house: str,
    bg_tasks: BackgroundTasks
):

    bg_tasks.add_task(
        send_raven,
        house
    )

    return {
        "message": "Raven dispatched."
    }
```

---

# 🎯 Final Learning Roadmap

```text
FastAPI Basics
      ↓
Routing & Parameters
      ↓
Pydantic Models
      ↓
Dependency Injection
      ↓
SQLAlchemy Async
      ↓
Project Architecture
      ↓
Authentication (JWT)
      ↓
Background Tasks
      ↓
Production Deployment
```

---

## 🎉 Congratulations

After mastering these phases, you'll be able to build:

* REST APIs
* Authentication Systems
* Production Backends
* Microservices
* SaaS Platforms
* AI/ML APIs
* Enterprise Applications

using modern FastAPI best practices.
