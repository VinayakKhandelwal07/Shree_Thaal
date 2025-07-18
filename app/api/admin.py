from datetime import datetime
import json
from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from app.models import Order, Product, OrderItem
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Query,
    Request,
    Cookie,
    status,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.schemas import Product as ProductSchema
from app.core import config, security
from app.database import get_db
from app.api.auth import authenticate_admin, get_current_admin
from app.crud import (
    get_all_orders,
    get_order,
    update_order_status,
    get_product,
    create_product,
    update_product_availability,
    update_product,
    delete_product,
    get_sales_report,
)
from app.schemas import (
    OrderResponse,
    OrderUpdate,
    # Order,
    ProductCreate,
    ProductUpdate,
    # Product,
    SalesReport,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    # Optional: Add auth dependency to protect all admin routes except login
    # dependencies=[Depends(get_current_admin)],
)

templates = Jinja2Templates(directory="frontend/templates")


# --- Admin Login Routes ---

@router.get("/login", response_class=HTMLResponse)
async def admin_login_get(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request, "error": None})


@router.post("/login", response_class=HTMLResponse)
async def admin_login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if not authenticate_admin(username, password):
        return templates.TemplateResponse(
            "admin_login.html",
            {"request": request, "error": "Invalid username or password"},
        )
    access_token = security.create_access_token(data={"sub": username})
    response = RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=3600,
        samesite="lax",
    )
    return response




@router.get("/dashboard", response_class=HTMLResponse, name="admin.dashboard")
async def admin_dashboard(
    request: Request,
    access_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if not access_token:
        return RedirectResponse(url="/admin/login")

    token = access_token.removeprefix("Bearer ")
    payload = security.decode_access_token(token)

    if not payload or payload.get("sub") != config.settings.ADMIN_USERNAME:
        return RedirectResponse(url="/admin/login")

    # ✅ Summary Data
    total_orders = db.query(Order).count()

    # Calculate total revenue from delivered orders only
    total_revenue = db.query(func.sum(Order.total_price)) \
        .filter(Order.status == "delivered") \
        .scalar() or 0.0

    # Filter pending and preparing orders for pending count
    pending_orders = db.query(Order).filter(Order.status.in_(["preparing", "accepted"])).count()

    # Count completed orders (delivered)
    completed_orders = db.query(Order).filter(Order.status == "delivered").count()

    # ✅ Top 5 Upcoming Orders (Pending or Placed)
    upcoming_orders = (
        db.query(Order)
        .filter(Order.status.in_(["placed", "Pending"]))
        .options(joinedload(Order.customer))  # load customer info
        .order_by(Order.created_at.desc())
        .limit(5)
        .all()
    )

    # ✅ Top 5 Products by Total Orders (from OrderItem)
    top_products_raw = (
        db.query(Product.name_en, func.count(OrderItem.id).label("total_orders"))
        .join(OrderItem, Product.id == OrderItem.product_id)
        .group_by(Product.id)
        .order_by(func.count(OrderItem.id).desc())
        .limit(5)
        .all()
    )

    top_products = [{"name": name, "orders": count} for name, count in top_products_raw]

    # ✅ Fetching Sales Report for Admin Dashboard
    sales_report = get_sales_report(db)

    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "admin": payload.get("sub"),
        "summary": {
            "total_orders": total_orders,
            "total_revenue": total_revenue,  # Only revenue from delivered orders
            "pending_orders": pending_orders,
            "completed_orders": completed_orders,
        },
        "recent_orders": upcoming_orders,
        "top_products": top_products,
        "sales_report": sales_report
    })




@router.get("/products", response_class=HTMLResponse)
def admin_products_page(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse("products.html", {"request": request, "products": products})


@router.post("/logout")
async def admin_logout():
    response = RedirectResponse(url="/", status_code=303)  # Redirect to home page "/"
    response.delete_cookie(key="access_token", path="/")
    return response


# --- Order Management ---

@router.get("/orders", response_class=HTMLResponse, name="admin.read_all_orders")
def read_all_orders(request:Request,db: Session = Depends(get_db)):
    """
    Get all customer orders.

    """
    orders = get_all_orders(db)
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})

@router.get("/orders/{order_id}", name="admin.get_order_details")
def get_order_details(request: Request, order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return templates.TemplateResponse("order_details.html", {
        "request": request,
        "order": order,
    })


@router.put("/orders/{order_id}/status", response_model=OrderResponse)
def change_order_status(
    order_id: int, status_update: OrderUpdate, db: Session = Depends(get_db)
):
    """
    Update order status: placed, accepted, preparing, delivered, cancelled.
    """
    updated_order = update_order_status(db, order_id, status_update.status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/orders/{order_id}", response_model=OrderResponse)
def delete_order(
    order_id: int, db: Session = Depends(get_db)
):
    """
    Delete an order by its ID.
    """
    order = get_order(db, order_id)  # Fetch the order to ensure it exists
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)  # Delete the order from the DB
    db.commit()  # Commit the transaction
    
    return order  # Return the deleted order for confirmati


# --- Product Management ---

@router.post("/products", response_model=ProductSchema, status_code=201,name="admin.add_product")
def add_product(
    name_en: str = Form(...),
    name_hi: str = Form(...),
    description: str = Form(...),
    price_per_kg: float = Form(...),
    image_url: Optional[str] = Form(None),
    quantities_json: str = Form(...),
    db: Session = Depends(get_db)
):
    quantities = json.loads(quantities_json)
    new_product = create_product(
        db=db,
        name_en=name_en,
        name_hi=name_hi,
        description=description,
        price_per_kg=price_per_kg,
        image_url=image_url,
        quantities=quantities
    )
    response = RedirectResponse(url="/admin/products", status_code=303)
    response.set_cookie("flash", "Product added successfully!", max_age=5)
    return response

@router.put("/products/{product_id}", response_model=ProductSchema, name="admin.update_product_details")
def update_product_details(
    product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)
):
    product = update_product(db, product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



@router.delete("/products/{product_id}", name="admin.remove_product")
def remove_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product from the catalog.
    """
    deleted = delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}


@router.put("/products/{product_id}/availability", response_model=ProductSchema)
def set_product_availability(
    product_id: int,
    available: bool = Query(..., description="Set product availability status"),
    db: Session = Depends(get_db),
):
    """
    Enable or disable a product.
    """
    product = update_product_availability(db, product_id, available)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# --- Sales Report ---

@router.get("/sales", response_model=SalesReport)
def sales_report(db: Session = Depends(get_db)):
    """
    Generate a sales report summary.
    """
    return get_sales_report(db)
