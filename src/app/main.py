from fastapi import FastAPI, HTTPException
from schemes.item import Item as Item

app = FastAPI()
# from routers.router1 import router as router1
# app.include_router(router1)
# REST server почитать
# to do  connect swagger


@app.get("/")
async def root():
    return {"Alan": "Wake"}


# In-memory database (for demonstration purposes)
items = []

# Pydantic model for item data
# Create an item


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.get("/items")
def get_item(item_id: int):
    try:
        return items[item_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="item does not exists")


# Update an item
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    items[item_id] = item
    return item


# Delete an item
@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    deleted_item = items.pop(item_id)
    return deleted_item
