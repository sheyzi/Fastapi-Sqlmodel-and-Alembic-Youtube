from typing import Optional
from sqlmodel import SQLModel, Field


class ItemBase(SQLModel):
    name: str
    price: float


class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    name: Optional[str] = None
    price: Optional[float] = None


class ItemOut(ItemBase):
    id: int
