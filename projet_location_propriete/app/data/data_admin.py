from typing import Dict, List, Optional
from app.interface.model_view.model_view_location import LocationView
from app.interface.model_view.model_view_utilisateur import UtilisateursView
from .db import get_connection

def connectionfonction():
    connection = get_connection()
    if not connection:
        # print("Impossible d’établir une connexion à la base de données.") # Retiré car pas d'explications
        return None
    return connection


def get_all_locations() -> list[LocationView]:
    connection = connectionfonction()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Location;")
        clients = cursor.fetchall()
        return clients
    finally:
        connection.close()


def get_location_id(id: int) -> Optional[LocationView]:
    connection = connectionfonction()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM Location WHERE id = %s"
        cursor.execute(query, (id,))
        row = cursor.fetchone()

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
        return location
    finally:
        connection.close()


def get_all_utilisateurs() -> list[UtilisateursView]:
    connection = connectionfonction()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Utilisateur;")
        utilisateurs = cursor.fetchall()
        return utilisateurs
    finally:
        connection.close()


def get_utilisateur_avec_id(id: int) -> Optional[UtilisateursView]:
    connection = connectionfonction()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Utilisateur WHERE id = %s;"
        cursor.execute(query, (id,))
        # Correction: utilise fetchone() car on cherche un seul utilisateur par ID
        utilisateur = cursor.fetchone() 
        
        return utilisateur
    finally:
        connection.close()


def get_reservation() -> List[Dict]:
    connection = connectionfonction()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Reservation;")
        reservation = cursor.fetchall()
        return reservation
    finally:
        connection.close()


def get_reservation_avec_nom(nom: str) -> List[Dict]:
    connection = connectionfonction()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Reservation RIGHT JOIN Client ON Reservation.client_id = Client.id WHERE Client.nom = %s;"
        cursor.execute(query, (nom,))
        # Correction: utilise fetchall() pour retourner une liste, même si un seul résultat
        reservation = cursor.fetchall() 
        return reservation
    finally:
        connection.close()

def insert_location(data: dict) -> Optional[Dict]:
    connection = connectionfonction()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            INSERT INTO Location 
            (id_utilisateur, titre, DESCRIPTION, adresse, ville, pays, prixParNuit, disponibilite, capacite, type)
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
        return {**data, "id": location_id}
    
    finally:
        connection.close()


def insert_utilisateurs(data: dict) -> Optional[Dict]:
    connection = connectionfonction()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            INSERT INTO Utilisateur 
            (nom, email)
            VALUES (%s, %s)
        """
        values = (
            data["nom"],
            data["email"]
        )
        cursor.execute(query, values)
        connection.commit()
        location_id = cursor.lastrowid
        return {**data, "id": location_id}
    
    finally:
        connection.close()


def insert_reservation(data: dict) -> Optional[Dict]:
    connection = connectionfonction()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            INSERT INTO Reservation 
            (date_debut, date_fin, statut, montant_total, client_id, location_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data["date_debut"],
            data["date_fin"],
            data["statut"],
            data["montant_total"],
            data["client_id"],
            data["location_id"]
        )
        cursor.execute(query, values)
        connection.commit()
        location_id = cursor.lastrowid
        return {**data, "id": location_id}
    
    finally:
        connection.close()

def update_location(id, data) -> Optional[Dict]:
    connection = connectionfonction()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Location WHERE id=%s;", (id,))
        existing = cursor.fetchone()
        if not existing:
            return None
        query = """
            UPDATE Location SET
                id_utilisateur=%s,
                titre=%s,
                DESCRIPTION=%s,
                adresse=%s,
                ville=%s,
                pays=%s,
                prixParNuit=%s,
                disponibilite=%s,
                capacite=%s,
                type=%s
            WHERE id=%s
        """
        values = (
            data.get("id_utilisateur", existing["id_utilisateur"]),
            data.get("titre", existing["titre"]),
            data.get("description", existing["DESCRIPTION"]),
            data.get("adresse", existing["adresse"]),
            data.get("ville", existing["ville"]),
            data.get("pays", existing["pays"]),
            data.get("prixParNuit", existing["prixParNuit"]),
            data.get("disponibilite", existing["disponibilite"]),
            data.get("capacite", existing["capacite"]),
            data.get("type", existing["type"]),
            id
        )
        cursor.execute(query, values)
        connection.commit()
        cursor.execute("SELECT * FROM Location WHERE id=%s;", (id,))
        return cursor.fetchone()
    finally:
        connection.close()


def update_utilisateurs(id: int, data: dict) -> Optional[Dict]:
    connection = connectionfonction()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Utilisateur WHERE id=%s;", (id,))
        existing = cursor.fetchone()
        if not existing:
            return None
        query = """
            UPDATE Utilisateur SET
                nom=%s,
                email=%s
            WHERE id=%s
        """
        values = (
            data.get("nom", existing["nom"]),
            data.get("email", existing["email"]),
            id
        )
        cursor.execute(query, values)
        connection.commit()
        cursor.execute("SELECT * FROM Utilisateur WHERE id=%s;", (id,))
        return cursor.fetchone()
    finally:
        connection.close()


def update_reservation(id: int, data: dict) -> Optional[Dict]:
    connection = connectionfonction()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Reservation WHERE id=%s;", (id,))
        existing = cursor.fetchone()
        if not existing:
            return None
        query = """
            UPDATE Reservation SET
                date_debut=%s,
                date_fin=%s,
                statut=%s,
                montant_total=%s,
                client_id=%s,
                location_id=%s
            WHERE id=%s
        """
        values = (
            data.get("date_debut", existing["date_debut"]),
            data.get("date_fin", existing["date_fin"]),
            data.get("statut", existing["statut"]),
            data.get("montant_total", existing["montant_total"]),
            data.get("client_id", existing["client_id"]),
            data.get("location_id", existing["location_id"]),
            id
        )
        cursor.execute(query, values)
        connection.commit()
        cursor.execute("SELECT * FROM Reservation WHERE id=%s;", (id,))
        return cursor.fetchone()
    finally:
        connection.close()

def delete_location_id(id: int) -> Optional[Dict]:
    connection = connectionfonction()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM Location WHERE id=%s;", (id,))
        location_existante = cursor.fetchone()
        if not location_existante:
            return None
        cursor.execute("DELETE FROM Location WHERE id=%s;", (id,))
        connection.commit()
        return {"message": f"Location avec id {id} supprimée"}
    finally:
        connection.close()

def delete_utilisateurs_id(id: int) -> Optional[Dict]:
    connection = connectionfonction()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM Utilisateur WHERE id=%s;", (id,))
        utilisateur_existante = cursor.fetchone()
        if not utilisateur_existante:
            return None
        cursor.execute("DELETE FROM Utilisateur WHERE id=%s;", (id,))
        connection.commit()
        return {"message": f"Utilisateur avec id {id} supprimée"}
    finally:
        connection.close()

def delete_reservation_id(id: int) -> Optional[Dict]:
    connection = connectionfonction()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM Reservation WHERE id=%s;", (id,))
        reservation_existante = cursor.fetchone()
        if not reservation_existante:
            return None
        cursor.execute("DELETE FROM Reservation WHERE id=%s;", (id,))
        connection.commit()
        return {"message": f"Reservation avec id {id} supprimée"}
    finally:
        connection.close()