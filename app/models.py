from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base  # import Base from your database module


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_number = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")


class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String, nullable=False)
    name_hi = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price_per_kg = Column(Float, nullable=False)
    quantities = Column(JSON, nullable=False)  # e.g., [{"weight": "250g", "multiplier": 0.25}]
    available = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete")


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="placed")  # placed, accepted, preparing, delivered, canceled
    total_price = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)  # cod, upi, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)  # total quantity units (like 1, 2 pieces of 250g)
    weight_selected = Column(String, nullable=False)  # e.g., "250g"
    price_per_kg = Column(Float, nullable=False)
    price_final = Column(Float, nullable=False)  # actual price based on multiplier

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
