from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Example model for request body validation


class Item(BaseModel):
    name: str
    description: str = None


# Root route


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


# Route with query parameter


@app.get("/greet/")
def greet(name: str = Query(..., description="Name to greet")):
    return {"message": f"Hello, {name}!"}


# Route with path parameter


@app.get("/items/{item_id}")
def read_item(item_id: int = Path(..., title="Item ID")):
    return {"item_id": item_id}


# Route with request body and response model


@app.post("/create_item/")
def create_item(item: Item):
    return {"item": item}


# Route with error handling


@app.get("/items/{item_id}/info")
def item_info(item_id: int):
    if item_id < 1:
        raise HTTPException(status_code=400, detail="Item ID must be greater than 0")
    return {"item_id": item_id, "info": "Item information"}


# Catch-all route


@app.get("/items/")
def list_items():
    return {"message": "Listing all items"}


# Route with query parameters


@app.get("/search/")
def search_items(q: str = Query(None, title="Search query")):
    return {"query": q, "results": []}
