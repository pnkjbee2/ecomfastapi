from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os
from sqlalchemy.sql import text


# Create a SQLAlchemy engine and session
DATABASE_URL = "postgresql://postgres:hunybee123@localhost/mydatabase" #change username, password and databse name.
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Defining Product model and creating the products table:
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, default=datetime.now().isoformat())
    total_amount = Column(Float)
    user_address_city = Column(String)
    user_address_country = Column(String)
    user_address_zip_code = Column(String)
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer)
    bought_quantity = Column(Integer)
    order = relationship("Order", back_populates="items")

Base.metadata.create_all(bind=engine)

app = FastAPI()

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int

class OrderCreate(BaseModel):
    timestamp: str
    total_amount: float
    user_address_city: str
    user_address_country: str
    user_address_zip_code: str
    items: List["OrderItemCreate"]

class OrderItemCreate(BaseModel):
    product_id: int
    bought_quantity: int

class OrderItem(BaseModel):
    id: int
    product_id: int
    bought_quantity: int

    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int
    timestamp: str
    total_amount: float
    user_address_city: str
    user_address_country: str
    user_address_zip_code: str
    items: List[OrderItem]

    class Config:
        orm_mode = True

@app.get("/products")
def get_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products

@app.post("/orders", response_model=Order)
def create_order(order: OrderCreate):
    db = SessionLocal()
    try:
        # Check if products are available and update quantities
        for item in order.items:
            product = db.query(Product).get(item.product_id)
            if product:
                if item.bought_quantity <= product.quantity:
                    product.quantity -= item.bought_quantity
                else:
                    raise HTTPException(status_code=400, detail=f"Not enough quantity available for product with ID {item.product_id}")
            else:
                raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")

        # Calculate total amount
        total_amount = sum(
            item.bought_quantity * db.query(Product.price).filter(Product.id == item.product_id).scalar()
            for item in order.items
        )

        # Save the order to the database
        new_order = Order(
            timestamp=order.timestamp,
            total_amount=total_amount,
            user_address_city=order.user_address_city,
            user_address_country=order.user_address_country,
            user_address_zip_code=order.user_address_zip_code,
            items=[OrderItem(product_id=item.product_id, bought_quantity=item.bought_quantity) for item in order.items]
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        db.close()

        return new_order

    except Exception as e:
        db.rollback()
        db.close()
        raise e

@app.get("/orders")
def get_orders(limit: int = 10, offset: int = 0):
    db = SessionLocal()
    orders = db.query(Order).offset(offset).limit(limit).all()
    db.close()
    return orders

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    db = SessionLocal()
    order = db.query(Order).get(order_id)
    db.close()
    if order:
        return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/products/{product_id}")
def update_product(product_id: int, quantity: int):
    db = SessionLocal()
    product = db.query(Product).get(product_id)
    if product:
        product.quantity = quantity
        db.commit()
        db.close()
        return {"message": "Product updated successfully"}
    db.close()
    raise HTTPException(status_code=404, detail="Product not found")

# Load and execute SQL file
with open(os.path.join(os.path.dirname(__file__), "sample_data.sql"), "r") as sql_file:
    sql_statements = sql_file.read().split(';')

    with engine.connect() as connection:
        for statement in sql_statements:
            if statement.strip():
                connection.execute(text(statement.strip()))



