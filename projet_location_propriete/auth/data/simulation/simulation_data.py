from app.data.models.model_users import User
from datetime import datetime
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

users: list[User] = [
    User(
        identifier=1,
        username="Hwei",
        full_name="Hwei Martin",
        email="Hwei@test.com",
        role="client",
        hashed_password=hash_password("Hwei@2025"),
        created_at=datetime.now()
    ),
    User(
        identifier=2,
        username="Mike",
        full_name="Mike Dupont",
        email="Mike@test.com",
        role="proprietaire",
        hashed_password=hash_password("Mike@2025"),
        created_at=datetime.now()
    ),
    
    User(
        identifier=2,
        username="Mat",
        full_name="Mat Dupont",
        email="Mat@test.com",
        role="proprietaire",
        hashed_password=hash_password("Mat@2025"),
        created_at=datetime.now()
    ),

    User(
        identifier=2,
        username="Admin Joe",
        full_name="Admin Joe",
        email="Joe@test.com",
        role="admin",
        hashed_password=hash_password("Joe@2025"),
        created_at=datetime.now()
    ),
]
