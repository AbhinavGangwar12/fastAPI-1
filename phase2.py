from fastapi import FastAPI, status, HTTPException

inventory = {
    "name": "Ser Duncan the Tall", 
    "gear": ["longsword", "shield", "plate armor"],
    "skills": ["swordsmanship", "horsemanship", "chivalry"],
    "horses": ["Brown Beauty", "Silver Streak"]
}

app = FastAPI(title="Hedge Knight API", version="1.0", description="An API for the Hedge Knight world")

@app.get("/inventory", status_code=status.HTTP_200_OK)
async def get_inventory(category: str | None = None):
    """
    Retrieve the inventory. Optional 'category' query filter (gear, skills, horses).
    """
    if category:
        category_lowercased = category.lower()
        if category_lowercased in inventory:
            return {category_lowercased: inventory[category_lowercased]}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Category '{category}' not found in inventory."
            )
            
    return inventory

@app.post("/horses", status_code=status.HTTP_201_CREATED)
async def add_horse(horse_name: str):
    """
    Add a new horse to Ser Duncan's stables.
    """
    if horse_name in inventory["horses"]:
        return {"message": f"Horse '{horse_name}' is already in the inventory."}
        
    inventory["horses"].append(horse_name)
    return {"message": f"Horse '{horse_name}' added to inventory."}

@app.delete("/horses/{horse_name}", status_code=status.HTTP_200_OK)
async def remove_horse(horse_name: str):
    """
    Remove a horse by name. Raises 404 if the horse doesn't exist.
    """
    if horse_name in inventory["horses"]:
        inventory["horses"].remove(horse_name)
        return {"message": f"Horse '{horse_name}' removed from inventory."}
    
    # Properly raise a 404 error if the horse isn't there
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Horse '{horse_name}' not found in inventory."
    )