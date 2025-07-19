from itertools import product
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.api.customer import router as customer_router 
from app.api.admin import router as admin_router  # adjust import path
 # adjust import path
from app.api import customer, admin, auth

from app.crud import get_all_products
from app.database import engine, Base, get_db  # Adjust path if needed

app = FastAPI(
    title="Sweet Shop Ordering System",
    description="API for QR code menu, ordering, and admin management",
    version="1.0.0",
)
# Path to your frontend directory
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "templates"

templates = Jinja2Templates(directory=str(FRONTEND_DIR))

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(customer_router)
app.include_router(admin.router)


# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request, db: Session = Depends(get_db), lang: str = "en"):
    sweets = get_all_products(db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "sweets": sweets
    })


# Create all tables in the database on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
