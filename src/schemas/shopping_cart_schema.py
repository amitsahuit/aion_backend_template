from pydantic import BaseModel


class ShoppingCartBase(BaseModel):
    shopping_id: int
    product_id: int
    Product_name: str
    owner_id: int


class ShoppingCartCreate(ShoppingCartBase):
    pass
