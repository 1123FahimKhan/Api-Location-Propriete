from fastapi import APIRouter, HTTPException, status, Body, Depends
from app.services import service_client
from app.interface.model_view.model_view_location import LocationView
from app.utils.auth import require_role
from app.services.services_user import get_current_user 
from app.interface.context.user_context import UserContext
from typing import Dict, Any, List

router = APIRouter(
    prefix="/client", 
    tags=["client"],
    dependencies=[Depends(require_role("client", "proprietaire", "admin"))] 
)

@router.get("/location", response_model=List[LocationView])
def get_locations_client(current_user: UserContext = Depends(get_current_user)):
    try:
        return service_client.lister_location_par_proprietaire(current_user.username) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/location/{id}", response_model=LocationView)
def get_location_id_client(id: int, current_user: UserContext = Depends(get_current_user)):
    try:
        return service_client.obtenir_location_avec_id(id, current_user.username) 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/location", 
             status_code=status.HTTP_201_CREATED,
             response_model=LocationView)
def add_location_client(data: dict = Body(...), current_user: UserContext = Depends(get_current_user)):
    try:
        return service_client.ajouter_location(data, current_user.username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reservation", response_model=List[Dict[str, Any]])
def get_reservations_client(current_user: UserContext = Depends(get_current_user)):
    try:
        return service_client.obtenir_reservations_par_client(current_user.username) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))