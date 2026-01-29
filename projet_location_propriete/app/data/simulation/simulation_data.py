from app.data.models.model_users import User
from datetime import datetime
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

users: list[User] = [
    User(
        identifier=301, # Correspond à l'Admin Joe (301)
        username="adminjoe",
        full_name="Admin Joe",
        email="admin.joe@email.com",
        role="admin",
        hashed_password=hash_password("adminjoe#2025"), # Assurez-vous d'utiliser le mot de passe réel pour le hash
        created_at=datetime.now()
    ),
    User(
        identifier=201, 
        username="mike",
        full_name="Mike The Proprietor",
        email="mike.p@email.com", # Correspond à l'email utilisé dans le script BD
        role="proprietaire",
        hashed_password=hash_password("mike@2025"), # Assurez-vous d'utiliser le mot de passe réel pour le hash
        created_at=datetime.now()
    ),
    User(
        identifier=400, # Mat est propriétaire (400)
        username="mat",
        full_name="Mat",
        email="mathematique101@mat.com",
        role="proprietaire",
        hashed_password=hash_password("Mat@2025"), # Assurez-vous d'utiliser le mot de passe réel pour le hash
        created_at=datetime.now()
    ),
    User(
        identifier=103, # Hwei est client (103)
        username="hwei",
        full_name="Hwei",
        email="hwei.c@email.com",
        role="client",
        hashed_password=hash_password("hwei@2025"), # Assurez-vous d'utiliser le mot de passe réel pour le hash
        created_at=datetime.now()
    ),
]
