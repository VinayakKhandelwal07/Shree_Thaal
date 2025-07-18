from sqlalchemy.orm import Session,joinedload
from sqlalchemy import func
import pytz
from datetime import datetime
from typing import Optional, Dict, List
from app.models import Order as OrderModel, OrderItem as OrderItemModel, User as UserModel
from app.models import User, Product, Order, OrderItem
from app.schemas import ProductUpdate, GuestOrderInput, SalesReport

LOCAL_TZ = pytz.timezone("Asia/Kolkata")

def convert_to_local_time(utc_time: datetime) -> str:
    """ Helper function to convert UTC datetime to local timezone """
    if utc_time is None:
        return "N/A"
    utc_time = utc_time.replace(tzinfo=pytz.UTC)  # Make it timezone-aware (UTC)
    local_time = utc_time.astimezone(LOCAL_TZ)  # Convert to local timezone
    return local_time.strftime('%d %b %Y, %I:%M %p')  # Format as per your preference



# --- USER CRUD ---

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_contact(db: Session, contact_number: str) -> Optional[User]:
    return db.query(User).filter(User.contact_number == contact_number).first()

def create_user(db: Session, name: str, contact_number: str, address: str) -> User:
    db_user = User(
        name=name,
        contact_number=contact_number,
        address=address,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_address(db: Session, user_id: int, new_address: str) -> Optional[User]:
    user = get_user(db, user_id)
    if user:
        user.address = new_address
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> Optional[User]:
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user


# --- PRODUCT CRUD ---

def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()


def get_all_products(db: Session) -> List[Product]:
    return db.query(Product).filter().all()

def create_product(
    db: Session,
    name_en: str,
    name_hi: str,
    description: str,
    price_per_kg: float,
    quantities: List[dict],
    image_url: Optional[str] = None
) -> Product:
    quantities_json = [q if isinstance(q, dict) else q.dict() for q in quantities]

    product = Product(
        name_en=name_en,
        name_hi=name_hi,
        description=description,
        price_per_kg=price_per_kg,
        available=True,
        image_url=image_url,
        quantities=quantities_json,
        created_at=datetime.utcnow()
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
    product = get_product(db, product_id)
    if not product:
        return None
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def update_product_availability(db: Session, product_id: int, available: bool) -> Optional[Product]:
    product = get_product(db, product_id)
    if product:
        product.available = available
        db.commit()
        db.refresh(product)
    return product

def delete_product(db: Session, product_id: int) -> Optional[Product]:
    product = get_product(db, product_id)
    if product:
        db.delete(product)
        db.commit()
    return product


# --- ORDER CRUD ---
def get_order(db: Session, order_id: int) -> Optional[Order]:
    return (
        db.query(Order)
        .options(
            joinedload(Order.customer),        # Load the customer (User)
            joinedload(Order.items).joinedload(OrderItem.product)  # Load items + products
        )
        .filter(Order.id == order_id)
        .first()
    )

def get_all_orders(db: Session) -> List[Order]:
    orders = db.query(Order)\
        .options(
            joinedload(Order.customer),  # 👈 this ensures customer data is loaded
            joinedload(Order.items)      # 👈 also load items
        ).all()
    
    # Convert created_at for each order to local time
    for order in orders:
        order.created_at_local = convert_to_local_time(order.created_at)
    return orders


def get_orders_by_user(db: Session, user_id: int) -> List[Order]:
    return db.query(Order).filter(Order.customer_id == user_id).all()



def create_order(db: Session, order_data: GuestOrderInput) -> OrderModel:
    # Step 1: Get or create customer
    user = get_user_by_contact(db, order_data.contact_number)
    if not user:
        user = create_user(db, order_data.name, order_data.contact_number, order_data.address)

    # Step 2: Validate products and calculate total
    total_price = 0.0
    order_items = []

    for item in order_data.items:
        product = get_product(db, item.product_id)
        if not product:
            raise ValueError(f"Product ID {item.product_id} not found.")
        if not product.available:
            raise ValueError(f"Product '{product.name_en}' is unavailable.")

        matched_quantity = next((q for q in product.quantities if q["weight"] == item.weight_selected), None)
        if not matched_quantity:
            raise ValueError(f"Invalid weight '{item.weight_selected}' for product '{product.name_en}'.")

        multiplier = matched_quantity["multiplier"]
        price_final = product.price_per_kg * multiplier * item.quantity
        total_price += price_final

        order_items.append(OrderItemModel(
            product_id=product.id,
            quantity=item.quantity,
            weight_selected=item.weight_selected,
            price_per_kg=product.price_per_kg,
            price_final=price_final
        ))

    # Step 3: Create order first
    order = OrderModel(
        customer_id=user.id,
        total_price=total_price,
        payment_method=order_data.payment_method,
        status="placed",
        created_at=datetime.utcnow()
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Step 4: Add order items
    for item in order_items:
        item.order_id = order.id
        db.add(item)

    db.commit()
    db.refresh(order)
    

    return order



def update_order_status(db: Session, order_id: int, status: str) -> Optional[Order]:
    order = get_order(db, order_id)
    if order:
        order.status = status
        db.commit()
        db.refresh(order)
    return order

def delete_order(db: Session, order_id: int) -> Optional[Order]:
    order = get_order(db, order_id)
    if order:
        db.delete(order)
        db.commit()
    return order


# --- SALES REPORT ---

def get_sales_report(db: Session) -> SalesReport:
    # Total number of orders
    total_orders = db.query(func.count(Order.id)).scalar() or 0
    
    # Calculate total revenue from only delivered orders (filtered by 'delivered' status)
    total_revenue = db.query(func.sum(Order.total_price)) \
        .filter(Order.status == 'delivered') \
        .scalar() or 0.0

    # Sales by product: sum the total price of items ordered for each product
    sales_by_product = (
        db.query(Product.name_en, func.sum(OrderItem.price_final))
        .join(OrderItem, Product.id == OrderItem.product_id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(Order.status == 'delivered')  # Only consider orders with 'delivered' status
        .group_by(Product.name_en)
        .all()
    )

    # Prepare sales report by product
    sales_dict: Dict[str, float] = {
        name_en: float(amount or 0.0) for name_en, amount in sales_by_product
    }

    return SalesReport(
        total_orders=total_orders,
        total_revenue=float(total_revenue),
        sales_by_product=sales_dict
    )
