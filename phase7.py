from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from datetime import datetime, timezone, timedelta
from typing import Annotated 

app = FastAPI(title="The Master of Whisperers API")

# Security configurations 
SECRET_KEY = "blood_and_cheese" 
ALGORITHM = "HS256"

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Checks for JWT token validity (tokenURL tells swaggerUI where to send the login request)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "varys" : {
        "username" : "varys",
        "hashed_password" : pwd_context.hash("littlebirds")
    }
}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token")
async def login(from_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(from_data.username)
    if not user_dict or not pwd_context.verify(from_data.password, user_dict["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user_dict["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

TokenDep = Annotated[str, Depends(oauth2_scheme)]

@app.get("/small-council/secrets")
async def read_secrets(token: TokenDep):
    return {"message": "The Queen's forces are maching up in the North. The Starks are gathering allies."}