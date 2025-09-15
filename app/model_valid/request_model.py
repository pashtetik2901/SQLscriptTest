from pydantic import BaseModel

class NewOrder(BaseModel):
    order_id: int
    product_id: int
    count: int