from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated 

app = FastAPI("Defense")


SECRET_KEY = "i_can_defend_the_realm"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_knight_db = {
    "Ser_Lancelot" : {
        "username" : "Ser_Lancelot",
        "hashed_password" : pwd_context.hash("sword123")
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_knight(username: str):
    return fake_knight_db.get(username)

def authenticate_knight(username: str, password: str):
    knight = get_knight(username)
    if not knight:
        return None
    if not verify_password(password, knight["hashed_password"]):
        return None
    return knight

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_knight(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise Exception("Invalid token")
    except jwt.PyJWTError:
        raise Exception("Invalid token")
    knight = get_knight(username)
    if not knight:
        raise Exception("Knight not found")
    return knight

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    knight = authenticate_knight(form_data.username, form_data.password)
    if not knight:
        raise Exception("Incorrect username or password")
    access_token = create_access_token(data={"sub" : knight["username"]})
    return {"access_token" : access_token, "token_type" : "bearer"}

@app.get("/defend")
async def defend(current_knight: Annotated[dict, Depends(get_current_knight)]):
    return {"message" : f"{current_knight['username']} is defending the realm!"}

@app.get("/")
async def read_root():
    return {"message" : "Welcome to the realm! Please log in to defend it."}