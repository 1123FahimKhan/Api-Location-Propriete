import datetime

from fastapi import HTTPException
from jose import jwt
from starlette import status

from auth.interface.model_view.model_view_token import TokenView
from auth.config.env import settings
from auth.interface.model_view.model_view_token_decoded import TokenViewDecoded


def issue_token(username : str) -> TokenView:
    token = create_access_token(username=username)
    return TokenView(access_token=token)

def create_access_token(username: str) -> str:
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def validate_token(token: str) -> TokenViewDecoded:
    decode_result = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    token_decoded = TokenViewDecoded(**decode_result)

    if token_decoded.exp < datetime.datetime.now(datetime.timezone.utc):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Expired token")

    return token_decoded