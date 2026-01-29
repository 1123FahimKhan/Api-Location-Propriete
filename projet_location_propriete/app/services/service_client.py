from app.data import data_client
from typing import List, Dict, Any

def _get_user_id_by_username(username: str) -> int:
    user_id = data_client.get_user_id_by_username(username)
    if user_id is None:
        raise ValueError(f"Utilisateur non trouvé pour le nom: {username}")
    return user_id

def lister_location_par_proprietaire(username: str) -> List[Dict[str, Any]]:
    owner_id = _get_user_id_by_username(username)
    
    location = data_client.get_locations_by_owner_id(owner_id)
    if location is None:
        raise Exception("Impossible de récupérer les locations.")
    return location

def obtenir_location_avec_id(id: int, username: str) -> Dict[str, Any]:
    owner_id = _get_user_id_by_username(username)
    
    if not id:
        raise ValueError("L'ID de la location est requis.")
        
    location_id = data_client.get_location_id_by_owner(id, owner_id)
    
    if location_id is None:
        raise Exception(f"Location non trouvée ou n'appartient pas à l'utilisateur: {id}")
    return location_id

def ajouter_location(data: dict, username: str) -> Dict[str, Any]:
    owner_id = _get_user_id_by_username(username)

    if not data:
        raise ValueError("Les données de la location sont requises.")
        
    data['id_utilisateur'] = owner_id
    location = data_client.insert_location(data)
    
    if not location:
        raise Exception("Impossible d'ajouter la location.")
    return location

def obtenir_reservations_par_client(username: str) -> List[Dict[str, Any]]:
    client_id = _get_user_id_by_username(username)
    
    reservation = data_client.get_reservations_by_client_id(client_id)
    
    if reservation is None:
        raise Exception("Impossible de récupérer les réservations")
    return reservation

def obtenir_reservation_avec_nom_client(nom: str, username: str) -> List[Dict[str, Any]]:
    owner_id = _get_user_id_by_username(username)
    
    if not nom:
        raise ValueError("Le nom du client est requis.")
        
    reservation = data_client.get_reservation_avec_nom_client_et_proprietaire(nom, owner_id)

    if reservation is None:
        raise Exception(f"Impossible de récupérer la réservation pour le client: {nom}")
    return reservation