from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, status, Body, Depends, Query
from app.services import service_admin
from app.interface.model_view.model_view_location import LocationView
from app.interface.model_view.model_view_utilisateur import UtilisateursView
from app.utils.auth import require_role # Assurez-vous que ce module existe et fonctionne

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    # Applique la dépendance à toutes les routes de ce routeur
    dependencies=[Depends(require_role("admin"))] 
)

# ==================================      GET

@router.get("/location", response_model=list[LocationView])
def get_locations():
    try:
        return service_admin.lister_locations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/location/{id}", response_model=LocationView)
def get_location_id(id: int):
    try:
        return service_admin.obtenir_location_avec_id(id)
    except ValueError as e:
        # 404 est plus approprié pour "Non trouvé par ID"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/utilisateurs", response_model=list[UtilisateursView])
def get_utilisateurs():
    try:
        return service_admin.obtenir_utilisateurs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/utilisateurs/{id}", response_model=UtilisateursView)
def get_utilisateur_id(id: int):
    try:
        return service_admin.obtenir_utilisateurs_avec_id(id)
    except ValueError as e:
        # 404 est plus approprié pour "Non trouvé par ID"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reservation", response_model=List[Dict[str, Any]])
def get_reservations():
    try:
        return service_admin.obtenir_reservations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reservation/nom", response_model=List[Dict[str, Any]])
def get_reservation_nom(nom: str = Query(..., description="Nom du client")):
    try:
        return service_admin.obtenir_reservation_avec_nom_client(nom)
    except ValueError as e:
        # 404 si aucune réservation trouvée pour le nom, 400 si nom manquant (si non géré par Query)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================================      POST

@router.post("/location", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
def create_location(data: dict = Body(...)):
    try:
        return service_admin.ajouter_location(data)
    except ValueError as e:
        # 400 est approprié pour les données d'entrée manquantes ou invalides
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/utilisateurs", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
def create_utilisateurs(data: dict = Body(...)):
    try:
        return service_admin.ajouter_utilisateurs(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reservation", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
def create_reservation(data: dict = Body(...)):
    try:
        return service_admin.ajouter_reservation(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================================      PUT

@router.put("/location/{id}", status_code=status.HTTP_200_OK, response_model=Dict[str, Any])
def modify_location(id: int, data: dict = Body(...)):
    try:
        return service_admin.modifier_location(id, data)
    except ValueError as e:
        # 404 si l'ID n'existe pas, 400 si les données sont invalides
        if "non trouvée" in str(e):
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/utilisateurs/{id}", status_code=status.HTTP_200_OK, response_model=Dict[str, Any])
def modify_utilisateurs(id: int, data: dict = Body(...)):
    try:
        return service_admin.modifier_utilisateurs(id, data)
    except ValueError as e:
        # 404 si l'ID n'existe pas, 400 si les données sont invalides
        if "non trouvé" in str(e):
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/reservation/{id}", status_code=status.HTTP_200_OK, response_model=Dict[str, Any])
def modify_reservation(id: int, data: dict = Body(...)):
    try:
        return service_admin.modifier_reservation(id, data)
    except ValueError as e:
        # 404 si l'ID n'existe pas, 400 si les données sont invalides
        if "non trouvée" in str(e):
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================================      DELETE

@router.delete("/location/{id}", status_code=status.HTTP_200_OK)
def delete_location(id: int):
    try:
        return service_admin.delete_location(id)
    except ValueError as e:
        # 404 est approprié si la ressource à supprimer n'existe pas
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/utilisateurs/{id}", status_code=status.HTTP_200_OK)
def delete_utilisateurs(id: int):
    try:
        return service_admin.delete_utilisateurs(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/reservation/{id}", status_code=status.HTTP_200_OK)
def delete_reservation(id: int):
    try:
        return service_admin.delete_reservation(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))