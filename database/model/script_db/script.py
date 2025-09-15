from database.model.simply_db_conn import OrderItem, Session
from app.model_valid.request_model import NewOrder
from sqlalchemy import select, and_

def add_product(data: NewOrder):
    stmt = select(OrderItem).where(and_(
        OrderItem.order_id == data.order_id,
        OrderItem.product_id == data.product_id,
    ))
    with Session() as session:
        result = session.execute(stmt)
        order_item: OrderItem | None = result.scalars().first()
        if order_item:
            try:
                order_item.quantity += data.count
                session.commit()
            except Exception as err:
                print(f'Error - {err}')
                session.rollback()
            
        else:
            new_order_item = OrderItem(
                order_id = data.order_id,
                product_id = data.product_id,
                quantity = data.count
            )
            
            try:
                session.add(new_order_item)
                session.commit()
            except Exception as err:
                print(f'Error - {err}')
                session.rollback()
            
