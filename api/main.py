from fastapi import FastAPI, HTTPException
from . import models, crud, schemas

app = FastAPI()

@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int):
    item = crud.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate):
    return crud.create_item(item)
