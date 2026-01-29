from app.data import data_locations

def lister_locations():
    locations = data_locations.get_all_locations()
    if locations is None:
        raise Exception("Impossible de récupérer les locations.")
    return locations


def obtenir_location_avec_id(id: int):
    if not id:
        raise ValueError("id est requis.")
    location_id = data_locations.get_location_id(id)

    if not location_id:
        raise ValueError("Location introuvable")
    return location_id
