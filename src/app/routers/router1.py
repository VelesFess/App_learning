from fastapi import APIRouter, FastAPI, HTTPException

from schemas.item import Item as Item

app = FastAPI()


# In-memory database (for demonstration purposes)
items: list[dict] = []

# Pydantic model for item data
# Create an item

router = APIRouter()


@router.get("/")
async def root():
    return {"Alan": "Wake"}


@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@router.get("/items")
def get_item(item_id: int):
    try:
        return items[item_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="item does not exists")


# Update an item
@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    items[item_id] = item
    return item


# Delete an item
@router.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    deleted_item = items.pop(item_id)
    return deleted_item
