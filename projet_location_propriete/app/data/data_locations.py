from app.interface.model_view.model_view_location import LocationView
from .db import get_connection

def connectionfonction():
    connection = get_connection()
    if not connection:
        print("Impossible d’établir une connexion à la base de données.")
        return None
    return connection

def get_all_locations() -> list[LocationView]:
    connection = connectionfonction()

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Location;")
    clients = cursor.fetchall()

    cursor.close()
    connection.close()
    return clients


def get_location_id(id: int) -> LocationView:
    connection = connectionfonction()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM Location WHERE id = %s"
    cursor.execute(query, (id,))
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if not row:
        return None

    location = LocationView(
        id=row["id"],
        id_utilisateur=row["id_utilisateur"],
        titre=row["titre"],
        DESCRIPTION=row["DESCRIPTION"],
        adresse=row["adresse"],
        ville=row["ville"],
        pays=row["pays"],
        prixParNuit=float(row["prixParNuit"]),
        disponibilite=row["disponibilite"].capitalize(),
        capacite=row["capacite"],
        type=row["type"].capitalize()
    )

    # print("valeur retournée :", location)
    # print("dict :", location.model_dump())

    return location
