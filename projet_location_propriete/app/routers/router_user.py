from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.data.data_users import convert_to_user_view
from app.interface.model_view.model_view_token import TokenView
from app.interface.model_view.model_view_user import UserView
from app.services.model.model_users import UserCreation
from app.services.services_auth import authenticate_and_issue_token
from app.services.services_user import create_user, list_users, get_current_user

router = APIRouter(prefix="/users", tags=["/users"])

"""
Paramètre(s) : form_data (OAuth2PasswordRequestForm)
    form_data.username: str
    form_data.password: str
Valeur(s) de retour : ( Jeton d'accès JWT )
    JSON : {
        access_token: str
        token_type: str
    }
code de retour : 200
"""
@router.post("/login", summary="Login a user")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenView:
    return authenticate_and_issue_token(username=form_data.username, password=form_data.password)


"""
Paramètre(s) : user (UserCreation)
    JSON : {
        full_name: str
        username: str
        email: EmailStr
        role: str
        password: SecretStr
    }
Valeur(s) de retour : ( Vue de l'utilisateur créé )
    JSON : {
        identifier: int
        username: str
        full_name: str
        email: EmailStr
        role: str
        created_at: datetime
    }
code de retour : 201
"""
@router.post("/register", status_code=201, summary="Register a new user")
def register_user(user: UserCreation) -> UserView:
    return convert_to_user_view(create_user(user))


"""
Paramètre(s) : null (Requiert l'authentification)
Valeur(s) de retour : ( Liste de toutes les vues utilisateurs )
    JSON : [
        {
            identifier: int
            username: str
            full_name: str
            email: EmailStr
            role: str
            created_at: datetime
        }
    ]
code de retour : 200
"""
@router.get("/list",
            summary="List users (requires auth)",
            dependencies=[Depends(get_current_user)])
def get_users() -> list[UserView]:
    return list_users()
