from fastapi import FastAPI, status

app = FastAPI(title="The Hedge Knight API")

squires = [{
    "id" : 1,
    "name" : "Tobho Mott",
    "status" : "active"
}]

@app.get("/squires/{squire_id}", status_code=status.HTTP_200_OK)
async def get_squire(squire_id: int):
    for squire in squires:
        if squire["id"] == squire_id:
            return squire
    return {"error" : "Squire not found"}

#Query parameter 
# URL: /knights/search?title=Ser&region=Reach
@app.get("/knights/search", status_code=status.HTTP_200_OK)
async def search_knight(title: str = "Ser", region: str | None = None):
    return {
        "search_parameters" : {
            'title' : title,
            'region' : region
        },
        'results' : ["Ser Duncan the Tall", "Ser Arlan of Pennytree"]
    }

# Post with explicit status code 
# URL: /tourneys
@app.post("/tourneys", status_code=status.HTTP_201_CREATED)
async def create_tourney(name: str, location: str):
    return {
        "message" : f"Ser Duncan has entered the {name} tourney at {location}!"
    }