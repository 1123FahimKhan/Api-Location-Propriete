from .db import get_connection
from typing import Dict, List, Optional
from mysql.connector import Error

def connectionfonction():
    connection = get_connection()
    if not connection:
        return None
    return connection

def lister_location_par_utilisateur(owner_id: int) -> List[Dict]:
    connection = connectionfonction()
    if not connection:
        return []

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Location WHERE id_utilisateur = %s;", (owner_id,))
        locations = cursor.fetchall()
        return locations
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_location_raw(id: int) -> Optional[Dict]:
    connection = connectionfonction()
    if not connection:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Location WHERE id = %s;", (id,))
        location = cursor.fetchone()
        return location
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def ajouter_location(data: dict) -> Dict:
    connection = connectionfonction()
    if not connection:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            INSERT INTO Location 
            (id_utilisateur, titre, description, adresse, ville, pays, prixParNuit, disponibilite, capacite, type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data["id_utilisateur"],
            data["titre"],
            data["description"],
            data["adresse"],
            data["ville"],
            data["pays"],
            data["prixParNuit"],
            data["disponibilite"],
            data["capacite"],
            data["type"]
        )
        cursor.execute(query, values)
        connection.commit()
        location_id = cursor.lastrowid
        return get_location_raw(location_id)
    except Error as e:
        print(f"Erreur SQL lors de l'ajout de location: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def modifier_location(id: int, data: dict) -> Optional[Dict]:
    connection = connectionfonction()
    if not connection:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        
        fields = []
        values = []
        for key, value in data.items():
            fields.append(f"{key} = %s")
            values.append(value)
        
        if not fields:
            return get_location_raw(id)

        query = f"UPDATE Location SET {', '.join(fields)} WHERE id = %s"
        values.append(id)

        cursor.execute(query, tuple(values))
        connection.commit()
        
        if cursor.rowcount == 0:
            return None
            
        return get_location_raw(id)
    except Error as e:
        print(f"Erreur SQL lors de la modification de location: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def supprimer_location(id: int) -> Optional[Dict]:
    connection = connectionfonction()
    if not connection:
        return None

    cursor = None
    try:
        location_to_delete = get_location_raw(id)
        if not location_to_delete:
            return None

        cursor = connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM Location WHERE id = %s;", (id,))
        connection.commit()
        
        if cursor.rowcount == 0:
            return None

        return {"message": f"Location avec id {id} supprimée", "location_supprimee": location_to_delete}
    except Error as e:
        print(f"Erreur SQL lors de la suppression de location: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
def obtenir_reservations_pour_proprietaire(owner_id: int) -> List[Dict]:
    connection = connectionfonction()
    if not connection:
        return []

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT r.* FROM Reservation r
            INNER JOIN Location l ON r.location_id = l.id
            WHERE l.id_utilisateur = %s;
        """
        cursor.execute(query, (owner_id,))
        reservations = cursor.fetchall()
        return reservations
    except Error as e:
        print(f"Erreur de lecture de réservations dans la base de données: {e}")
        return [] 
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def obtenir_reservation_avec_nom_client(nom: str, owner_id: int) -> List[Dict]:
    connection = connectionfonction()
    if not connection:
        return []

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT r.* FROM Reservation r
            INNER JOIN Client c ON r.client_id = c.id
            INNER JOIN Location l ON r.location_id = l.id
            WHERE c.nom = %s AND l.id_utilisateur = %s;
        """
        cursor.execute(query, (nom, owner_id))
        reservations = cursor.fetchall()
        return reservations
    except Error as e:
        print(f"Erreur de lecture de réservations par nom dans la base de données: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()