from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import select, create_engine
from app.config import setting

engine = create_engine(setting.DB_PATH)
Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

from sqlalchemy import (
    Column, Integer, String, Text, DECIMAL, ForeignKey, CheckConstraint,
    Index, TIMESTAMP, func, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    parent = relationship("Category", remote_side=[id], backref="children")

    __table_args__ = (
        Index("idx_categories_parent_id", "parent_id"),
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", backref="products")

    __table_args__ = (
        CheckConstraint(quantity >= 0, name="chk_quantity_nonnegative"),
        CheckConstraint(price >= 0, name="chk_price_nonnegative"),
        Index("idx_products_category", "category_id"),
    )


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=True)

    orders = relationship("Order", back_populates="client")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    order_date = Column(TIMESTAMP, server_default=func.current_timestamp())

    client = relationship("Client", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

    __table_args__ = (
        Index("idx_orders_client", "client_id"),
        Index("idx_orders_date", "order_date"),
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")

    __table_args__ = (
        CheckConstraint(quantity > 0, name="chk_quantity_positive"),
        UniqueConstraint("order_id", "product_id", name="unq_order_product"),
        Index("idx_order_items_order", "order_id"),
        Index("idx_order_items_product", "product_id"),
    )

