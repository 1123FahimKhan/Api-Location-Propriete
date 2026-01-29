import bcrypt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.data import data_users
from app.data.models.model_users import User
from app.interface.context.user_context import UserContext
from app.services.model.model_users import UserCreation
from app.services.services_auth import validate_token, get_password_hash

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserContext:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_decoded = validate_token(token)
    user_data = data_users.get_user_by_username(token_decoded.sub)
    
    if user_data is None:
        raise credentials_exception
        
    user = UserContext(
        username = user_data.username,
        role = user_data.role
    )

    return user


def create_user(payload: UserCreation) -> User:
    if data_users.get_user_by_username(payload.username) is not None:
        raise HTTPException(status_code=400, detail="Username already exists")
    if data_users.get_user_by_email(str(payload.email)) is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = get_password_hash(payload.password.get_secret_value())
    user = data_users.create_user(
        full_name=payload.full_name,
        username=payload.username,
        email=str(payload.email),
        role=payload.role,
        hashed_password=hashed,
    )

    return user


def list_users():
    return data_users.list_users_view()
