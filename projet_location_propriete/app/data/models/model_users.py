from datetime import datetime
from pydantic import BaseModel, field_validator, EmailStr


class User(BaseModel):
    identifier: int
    username: str
    full_name: str
    email: EmailStr
    role: str = "client"
    hashed_password: str
    created_at: datetime

    @field_validator("username")
    @classmethod
    def validate_username(cls, validate: str):
        if not validate or validate.strip() == "":
            raise ValueError("Le nom d'utilisateur ne peut pas être vide.")
        return validate