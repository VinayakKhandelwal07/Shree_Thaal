# app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from app.core import config, security

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# Response schema for JWT token
class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_admin(username: str, password: str) -> bool:
    """
    Verify admin credentials against stored username and hashed password.
    """
    if username != config.settings.ADMIN_USERNAME:
        return False
    # Verify_password expects the plain password and the stored hashed password
    if not security.verify_password(password, config.settings.ADMIN_PASSWORD_HASH):
        return False
    return True


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Admin login endpoint to obtain a JWT access token.
    """
    is_valid = authenticate_admin(form_data.username, form_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_admin(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependency for protecting routes - validates JWT and ensures admin identity.
    """
    payload = security.decode_access_token(token)
    if not payload or payload.get("sub") != config.settings.ADMIN_USERNAME:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload.get("sub")

