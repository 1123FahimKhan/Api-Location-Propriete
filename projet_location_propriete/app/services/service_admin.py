from app.data import data_admin
from app.interface.model_view.model_view_location import LocationView

# GET methods
def lister_locations():
    locations = data_admin.get_all_locations()
    if locations is None:
        raise Exception("Impossible de récupérer les locations.")
    return locations


def obtenir_location_avec_id(id: int) -> LocationView:
    if not id:
        raise ValueError("id est requis.")
    location = data_admin.get_location_id(id)
    if location is None:
        # ValueError pour que le router gère un "Not Found" (400 ou 404)
        raise ValueError(f"Location non trouvée avec l'id: {id}")
    return location

def obtenir_utilisateurs():
    utilisateurs = data_admin.get_all_utilisateurs()
    if utilisateurs is None:
        raise Exception("Impossible de récupérer les utilisateurs.")
    return utilisateurs

def obtenir_utilisateurs_avec_id(id: int):
    if not id:
        raise ValueError("id est requis.")
    utilisateurs = data_admin.get_utilisateur_avec_id(id)
    if utilisateurs is None:
        # ValueError pour que le router gère un "Not Found" (400 ou 404)
        raise ValueError(f"Utilisateur non trouvé avec l'id: {id}")
    return utilisateurs


def obtenir_reservations():
    reservation = data_admin.get_reservation()
    if reservation is None:
        raise Exception("Impossible de récupérer les réservations")
    return reservation

def obtenir_reservation_avec_nom_client(nom: str):
    if not nom:
        raise ValueError("nom du client est requis.")
    reservation = data_admin.get_reservation_avec_nom(nom)
    if reservation is None:
        # ValueError pour que le router gère un "Not Found" (400 ou 404)
        raise ValueError(f"Réservation non trouvée pour le nom du client: {nom}")
    return reservation

# POST methods
def ajouter_location(data: dict):
    if not data:
        raise ValueError("Les données de la location sont requises.")
    location = data_admin.insert_location(data)
    if location is None:
        raise Exception("Impossible d'ajouter la location (erreur base de données).")
    return location

def ajouter_utilisateurs(data: dict):
    if not data:
        raise ValueError("Les données de l'utilisateur sont requises.")
    utilisateur = data_admin.insert_utilisateurs(data)
    if utilisateur is None:
        raise Exception("Impossible d'ajouter l'utilisateur (erreur base de données).")
    return utilisateur

def ajouter_reservation(data: dict):
    if not data:
        raise ValueError("Les données de la reservation sont requises.")
    reservation = data_admin.insert_reservation(data)
    if reservation is None:
        raise Exception("Impossible d'ajouter la reservation (erreur base de données).")
    return reservation

# PUT methods
def modifier_location(id: int, data: dict):
    if not data:
        raise ValueError("Les données de la location sont requises.")
    location = data_admin.update_location(id, data)
    if location is None:
        # ValueError pour indiquer que l'ID n'a pas été trouvé pour la modification
        raise ValueError(f"Location non trouvée avec l'id: {id} pour la modification.")
    return location

def modifier_utilisateurs(id: int, data: dict):
    if not data:
        raise ValueError("Les données de l'utilisateur sont requises.")
    utilisateur = data_admin.update_utilisateurs(id, data)
    if utilisateur is None:
        # ValueError pour indiquer que l'ID n'a pas été trouvé pour la modification
        raise ValueError(f"Utilisateur non trouvé avec l'id: {id} pour la modification.")
    return utilisateur

def modifier_reservation(id: int, data: dict):
    if not data:
        raise ValueError("Les données de la reservation sont requises.")
    reservation = data_admin.update_reservation(id, data)
    if reservation is None:
        # ValueError pour indiquer que l'ID n'a pas été trouvé pour la modification
        raise ValueError(f"Réservation non trouvée avec l'id: {id} pour la modification.")
    return reservation

# DELETE methods
def delete_location(id: int):
    location = data_admin.delete_location_id(id)
    if location is None:
        # ValueError pour indiquer que l'ID n'a pas été trouvé pour la suppression
        raise ValueError(f"Location non trouvée avec l'id: {id} pour la suppression.")
    return location

def delete_utilisateurs(id: int):
    utilisateur = data_admin.delete_utilisateurs_id(id)
    if utilisateur is None:
        # ValueError pour indiquer que l'ID n'a pas été trouvé pour la suppression
        raise ValueError(f"Utilisateur non trouvé avec l'id: {id} pour la suppression.")
    return utilisateur

def delete_reservation(id: int):
    reservation = data_admin.delete_reservation_id(id)
    if reservation is None:
        # ValueError pour indiquer que l'ID n'a pas été trouvé pour la suppression
        raise ValueError(f"Réservation non trouvée avec l'id: {id} pour la suppression.")
    return reservation
