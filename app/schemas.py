from fastapi import Form
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


# --- Enums ---
class OrderStatus(str, Enum):
    placed = "placed"
    accepted = "accepted"
    preparing = "preparing"
    delivered = "delivered"
    cancelled = "cancelled"


# --- Quantity for Products ---
class Quantity(BaseModel):
    weight: str = Field(..., example="250g")
    multiplier: float = Field(..., gt=0, example=0.25)


# --- Product Schemas ---
class ProductBase(BaseModel):
    name_en: str = Field(..., example="Gulab Jamun")
    name_hi: str = Field(..., example="गुलाब जामुन")
    description: Optional[str] = Field(None, example="Sweet syrup soaked balls")
    price_per_kg: float = Field(..., gt=0, example=420.0)
    available: bool = Field(default=True)
    image_url: Optional[str] = Field(None, example="http://example.com/image.jpg")
    quantities: List[Quantity]

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name_en: Optional[str]
    name_hi: Optional[str]
    description: Optional[str]
    price_per_kg: Optional[float]
    available: Optional[bool]
    image_url: Optional[str]
    quantities: Optional[List[Quantity]]

class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Customer Schemas ---
class CustomerBase(BaseModel):
    name: str = Field(..., example="John Doe")
    contact_number: str = Field(..., example="+911234567890")
    address: str = Field(..., example="123 Sweet Street, City")

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Order Item Schemas ---
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, example=2)
    weight_selected: str = Field(..., example="500g")
    price_per_kg: float = Field(..., gt=0)
    price_final: float = Field(..., gt=0)


class ProductSummary(BaseModel):
    # id: int
    name_en: str

    class Config:
        from_attributes = True


class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    product: Optional[ProductSummary]  # Add this line to include product details


    class Config:
        from_attributes = True


# --- Guest Order Schemas ---
class GuestOrderItemInput(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    weight_selected: str = Field(..., example="250g")
    price: float = Field(..., gt=0)

class GuestOrderInput(BaseModel):
    name: str
    contact_number: str
    address: str
    payment_method: str = Field(..., pattern="^(cod|upi)$", example="cod")
    items: List[GuestOrderItemInput]

class GuestOrderResponse(BaseModel):
    order_id: int
    customer_id: int
    message: str = "Order placed successfully"


# --- Order Schemas ---
class OrderBase(BaseModel):
    customer_id: int

class OrderCreate(OrderBase):
    payment_method: str = Field(..., example="cod")
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = Field(None, example=OrderStatus.accepted.value)

class Order(OrderBase):
    id: int
    status: OrderStatus
    total_price: float = Field(..., gt=0)
    payment_method: str
    created_at: datetime
    items: List[OrderItem] = Field(default_factory=list)

    class Config:
        from_attributes = True

class OrderResponse(Order):
    customer: Optional[Customer] = None


# --- Admin Schemas ---
class AdminBase(BaseModel):
    username: str = Field(..., example="adminuser")

class AdminCreate(AdminBase):
    password: str = Field(..., min_length=6, example="securepassword123")

class Admin(AdminBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Payment Schemas ---
class PaymentBase(BaseModel):
    order_id: int
    amount: float = Field(..., gt=0, example=150.0)
    payment_method: str = Field(..., example="UPI")
    status: Optional[str] = Field("pending", example="completed")

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Sales Report Schema ---
class SalesReport(BaseModel):
    total_orders: int
    total_revenue: float
    sales_by_product: Dict[str, float]

    class Config:
        schema_extra = {
            "example": {
                "total_orders": 100,
                "total_revenue": 5000.00,
                "sales_by_product": {
                    "Gulab Jamun": 2500.00,
                    "Samosa": 1500.00,
                    "Chai": 1000.00,
                },
            }
        }
