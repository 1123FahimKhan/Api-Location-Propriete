from datetime import datetime

from app.data.models.model_users import User
from app.data.simulation.simulation_data import users
from app.interface.model_view.model_view_user import UserView


def convert_to_user_view(user: User) -> UserView:
    return UserView(
        id=user.identifier,
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        role=user.role,
        created_at=user.created_at
    )

def get_user_by_username(username: str) -> User | None:
    for user in users:
        if user.username == username:
            return user

    return None


def get_user_by_email(email: str) -> User | None:
    for user in users:
        if user.email == email:
            return user

    return None

def list_users_view() -> list[UserView]:
    users_view = []
    for user in users:
        users_view.append(convert_to_user_view(user))

    return users_view

def create_user(full_name: str, username: str, email: str, role:str, hashed_password: str) -> User:
    user = User(
        identifier=len(users),
        full_name=full_name,
        username=username,
        email=email,
        role=role,
        hashed_password=hashed_password,
        created_at=datetime.now()
    )

    users.append(user)
    return user

