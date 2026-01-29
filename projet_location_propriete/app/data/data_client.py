import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

load_dotenv()


def get_user_id_by_username(username: str) -> Optional[int]:
    if username == "hwei":
        return 201
    if username == "mike":
        return 101
    return None

def get_locations_by_owner_id(owner_id: int) -> Optional[List[Dict[str, Any]]]:
    if owner_id == 201:
        return [
            {"id": 1, "id_utilisateur": 201, "titre": "Maison de Hwei", "description": "Description...", "adresse": "Adresse...", "ville": "Ville...", "pays": "Pays...", "prixParNuit": 100.0, "disponibilite": "Disponible", "capacite": 4, "type": "Maison"},
            {"id": 2, "id_utilisateur": 201, "titre": "Studio de Hwei", "description": "Description...", "adresse": "Adresse...", "ville": "Ville...", "pays": "Pays...", "prixParNuit": 50.0, "disponibilite": "Disponible", "capacite": 1, "type": "Studio"},
        ]
    return []

def get_location_id_by_owner(location_id: int, owner_id: int) -> Optional[Dict[str, Any]]:
    if location_id == 1 and owner_id == 201:
        return {"id": 1, "id_utilisateur": 201, "titre": "Maison de Hwei", "description": "Description...", "adresse": "Adresse...", "ville": "Ville...", "pays": "Pays...", "prixParNuit": 100.0, "disponibilite": "Disponible", "capacite": 4, "type": "Maison"}
    return None

def insert_location(data: dict) -> Optional[Dict[str, Any]]:
    if data:
        new_id = 999 
        return {"id": new_id, **data}
    return None

def get_reservations_by_client_id(client_id: int) -> Optional[List[Dict[str, Any]]]:
    if client_id == 201:
        return [
            {"id": 50, "location_id": 10, "client_id": 201, "date_debut": "2025-12-01", "date_fin": "2025-12-10", "prix_total": 500.0},
        ]
    return []

def get_reservation_avec_nom_client_et_proprietaire(nom: str, owner_id: int) -> Optional[List[Dict[str, Any]]]:
    if nom == "Hwei" and owner_id == 201:
        return [
            {"id": 50, "location_id": 10, "client_id": 201, "nom_client": "Hwei", "date_debut": "2025-12-01", "date_fin": "2025-12-10", "prix_total": 500.0},
        ]
    return []