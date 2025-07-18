from typing import List
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import api
from app.database import get_db
from app.crud import get_all_products, create_order, get_order
from app.schemas import (
    GuestOrderInput,
    GuestOrderResponse,
    OrderResponse,
    Product
)

router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)


templates = Jinja2Templates(directory="frontend")  # adjust if needed



@router.get("/menu", response_model=List[Product])
def get_menu(db: Session = Depends(get_db)):
    """
    Fetch the list of available sweets/products.
    """
    return get_all_products(db)


@router.post("/order", response_model=GuestOrderResponse, status_code=201)
async def place_order(order_input: GuestOrderInput, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    print("Received JSON:", data)  # <-- log raw input to console
    try:
        order = create_order(db, order_input)
        return GuestOrderResponse(
            message="Order placed successfully.",
            order_id=order.id,
            customer_id=order.customer_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/order/{order_id}", response_model=OrderResponse)
def track_order(order_id: int, db: Session = Depends(get_db)):
    """
    Track an order using its order ID (API JSON).
    """
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# Optional: Track order form (for HTML response)
@router.get("/track", response_class=HTMLResponse)
def show_order_tracking_form(request: Request):
    return templates.TemplateResponse("track_form.html", {"request": request})


@router.post("/track", response_class=HTMLResponse)
async def show_order_tracking_result(
    request: Request,
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Display order details in HTML form based on the order ID.
    """
    order = get_order(db, order_id)
    if not order:
        return templates.TemplateResponse(
            "track_form.html", {"request": request, "error": "Order not found"}
        )
    return templates.TemplateResponse(
        "Order_Track.html", {"request": request, "order": order}
    )