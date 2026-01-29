from fastapi import HTTPException, Depends
from app.services.services_user import get_current_user

PERMISSIONS = {
    "admin": ["*"],
    "proprietaire": ["Location:read", "Location:write", "Reservation:read", "Paiement:read", "Proprietaire:read"],
    "client": ["Reservation:read", "Reservation:write", "Paiement:read", "Proprietaire:read"]
}

def require_role(*allowed_roles: str):
    def role_checker(user=Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Accès interdit"
            )
        return user
    return role_checker
