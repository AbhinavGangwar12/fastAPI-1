from fastapi import FastAPI

app = FastAPI(title="Hedge Knight API", version="1.0", description="An API for the Hedge Knight world")

@app.get("/")
async def root():
    return {"message": "Welcome to the Hedge Knight API!"}