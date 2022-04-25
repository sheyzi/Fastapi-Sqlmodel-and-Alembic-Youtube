from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from models import Item, ItemCreate, ItemOut, ItemUpdate
from datbase import create_db_and_tables, engine, get_db
from sqlmodel import Session


app = FastAPI()


@app.on_event("startup")
def startup():
    create_db_and_tables()


"""
DONE # GET /items/
# GET /items/{item_id}
DONE # POST /items/
# PUT /items/{item_id}
# DELETE /items/{item_id}
"""


@app.post("/items/", status_code=201, response_model=ItemOut)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    item = Item(**item.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items/", response_model=List[ItemOut])
def get_items(
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Item)
    if min_price:
        query = query.filter(Item.price >= min_price)
    if max_price:
        query = query.filter(Item.price <= max_price)
    if search:
        query = query.filter(Item.name.contains(search))
    return query.all()


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Item).get(item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = item.dict(exclude_unset=True)
    for key in item:
        setattr(db_item, key, item[key])
    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}
