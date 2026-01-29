import re

from pydantic import BaseModel, EmailStr, SecretStr, field_validator


class UserCreation(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    role: str
    password: SecretStr

    @field_validator("username")
    def validate_username(cls, v: str) -> str:
        if not re.fullmatch(r"[A-Za-z0-9_]{3,30}", v):
            raise ValueError("Username must be 3-30 chars: letters, numbers, underscore only.")
        return v

    @field_validator("password")
    def validate_password(cls, v: SecretStr) -> SecretStr:
        s = v.get_secret_value()
        if len(s) < 8:
            raise ValueError("Password must be at least 8 characters.")
        if not re.search(r"[A-Z]", s):
            raise ValueError("Password must include an uppercase letter.")
        if not re.search(r"[a-z]", s):
            raise ValueError("Password must include a lowercase letter.")
        if not re.search(r"[0-9]", s):
            raise ValueError("Password must include a number.")
        if not re.search(r"[^A-Za-z0-9]", s):
            raise ValueError("Password must include a special character.")
        return v
