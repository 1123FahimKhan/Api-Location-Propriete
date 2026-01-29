from fastapi import APIRouter, Depends, Form
from starlette import status

from auth.interface.model_view.model_view_token_decoded import TokenViewDecoded
from auth.services.services_auth import issue_token, validate_token

router = APIRouter(prefix="/token", tags=["auth"])

@router.post("/issue")
def authenticate(username : str = Form(...)):
    return issue_token(username)

@router.post("/validate")
def validate(token: str = Form(...)) -> TokenViewDecoded:
    return validate_token(token)
