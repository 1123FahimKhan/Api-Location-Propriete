from fastapi import APIRouter, HTTPException, status, Body, Depends, Query
from app.services import service_proprietaire
from app.interface.model_view.model_view_location import LocationView
from app.utils.auth import require_role
from app.services.services_user import get_current_user 
from app.interface.context.user_context import UserContext
from typing import Dict, Any, List

router = APIRouter(
    prefix="/proprietaire", 
    tags=["proprietaire"],
    dependencies=[Depends(require_role("admin", "proprietaire"))]
)

@router.get("/location", response_model=List[LocationView])
def get_locations(current_user: UserContext = Depends(get_current_user)):
    try:
        return service_proprietaire.lister_location(current_user.username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/location/{id}", response_model=LocationView)
def get_location_id(id: int, current_user: UserContext = Depends(get_current_user)):
    try:
        return service_proprietaire.obtenir_location_avec_id(id, current_user.username)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/location", 
            status_code=status.HTTP_201_CREATED,
            response_model=LocationView)
def add_location(data: dict = Body(...), current_user: UserContext = Depends(get_current_user)):
    try:
        data['id_utilisateur'] = service_proprietaire._get_owner_id_by_username(current_user.username)
        return service_proprietaire.ajouter_location(data, current_user.username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/location/{id}", 
            response_model=LocationView)
def update_location(id: int, data: Dict[str, Any] = Body(...), current_user: UserContext = Depends(get_current_user)):
    try:
        return service_proprietaire.modifier_location(id, data, current_user.username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/location/{id}", status_code=status.HTTP_200_OK)
def delete_location(id: int, current_user: UserContext = Depends(get_current_user)):
    try:
        return service_proprietaire.supprimer_location(id, current_user.username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reservation", response_model=List[Dict[str, Any]])
def get_reservations(current_user: UserContext = Depends(get_current_user)):
    try:
        return service_proprietaire.obtenir_reservations(current_user.username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reservation/nom", response_model=List[Dict[str, Any]])
def get_reservation_par_nom(nom: str = Query(...),
                            current_user: UserContext = Depends(get_current_user)):
    try:
        reservations = service_proprietaire.obtenir_reservation_avec_nom_client(nom, current_user.username)            
        return reservations
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))