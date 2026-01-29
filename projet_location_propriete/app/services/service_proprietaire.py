from fastapi import HTTPException, status
from app.data import data_proprietaire
from app.data import data_users
from typing import Dict, List, Any # FIX: Ajout de List pour les annotations de type

class LocationNotFoundException(Exception):
    pass
class PermissionDeniedException(Exception):
    pass

def _get_owner_id_by_username(username: str) -> int:
    user = data_users.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Utilisateur non trouvé ou non autorisé")
    return user.identifier


def _check_ownership(location_id: int, owner_id: int):
    location = data_proprietaire.get_location_raw(location_id)
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Location avec l'ID {location_id} non trouvée.")
    
    # FIX: Utilisation des crochets pour accéder à la clé du dictionnaire
    if location['id_utilisateur'] != owner_id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès non autorisé: Cette location ne vous appartient pas.")
    return location


def lister_location(username: str):
    try:
        owner_id = _get_owner_id_by_username(username)
        return data_proprietaire.lister_location_par_utilisateur(owner_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur de service lors de la récupération des locations: {e}")

def obtenir_location_avec_id(id: int, username: str):
    try:
        owner_id = _get_owner_id_by_username(username)
        return _check_ownership(id, owner_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur de service lors de la récupération de la location: {e}")

def ajouter_location(data: dict, username: str):
    try:
        owner_id = _get_owner_id_by_username(username)
        
        if data.get('id_utilisateur') != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="L'ID utilisateur dans les données ne correspond pas à l'utilisateur authentifié."
            )

        location = data_proprietaire.ajouter_location(data)
        if not location:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur lors de l'ajout de la location.")
        return location
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur de service lors de l'ajout : {e}")

def modifier_location(id: int, data: Dict[str, Any], username: str):
    try:
        owner_id = _get_owner_id_by_username(username)
        _check_ownership(id, owner_id)
        
        if 'id_utilisateur' in data and data['id_utilisateur'] != owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès non autorisé: Impossible de modifier l'id_utilisateur.")
        
        if 'id_utilisateur' in data:
            del data['id_utilisateur']

        location = data_proprietaire.modifier_location(id, data)
        if not location:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Impossible de modifier la location avec l'ID {id}.")
        return location
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur de service lors de la modification : {e}")


def supprimer_location(id: int, username: str):
    try:
        owner_id = _get_owner_id_by_username(username)
        _check_ownership(id, owner_id)
        
        return data_proprietaire.supprimer_location(id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur de service lors de la suppression : {e}")


def obtenir_reservations(username: str) -> List[Dict]:
    try:
        owner_id = _get_owner_id_by_username(username)
        return data_proprietaire.obtenir_reservations_pour_proprietaire(owner_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur de service : {e}")


def obtenir_reservation_avec_nom_client(nom: str, username: str) -> List[Dict]:
    try:
        owner_id = _get_owner_id_by_username(username)
        return data_proprietaire.obtenir_reservation_avec_nom_client(nom, owner_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur de service lors de la recherche par nom: {e}")