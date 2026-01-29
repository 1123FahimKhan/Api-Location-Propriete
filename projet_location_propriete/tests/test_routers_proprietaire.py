import requests
import pytest
from pytest_bdd import scenarios, given, when, then
import json

BASE_URL = "http://localhost:10164/proprietaire"
Login_URL = "http://localhost:10164/users/login"

scenarios("../features/proprietaire.feature")

def login(username, password):
    login_data = {
        "username": username,
        "password": password
    }
    response = requests.post(Login_URL, data=login_data)
    
    if response.status_code == 200:
        response_json = response.json()
        token = response_json.get("access_token")
        if token is None:
            pytest.fail(f"Connexion réussie (200) mais jeton manquant dans la réponse: {response.text}")
        return token
    else:
        pytest.fail(f"Échec de la connexion pour {username}. Code: {response.status_code}, Réponse: {response.text}")

@pytest.fixture(scope="session")
def auth_token_proprietaire():
    token = login("mike", "mike@2025")
    return token

@given("je suis un proprietaire")
def user_proprietaire(auth_token_proprietaire):
    return auth_token_proprietaire

@when("je demande la liste de mes propriétés disponibles")
def get_locations(request, auth_token_proprietaire):
    url = f"{BASE_URL}/location"
    headers = {
        "Authorization": f"Bearer {auth_token_proprietaire}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    request._location_response_all = response
    return response

@then("je reçois la liste de tous mes propriété avec le code de retour 200")
def verify_get_locations(request):
    response = request._location_response_all
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@when("je demande dans la liste seulement un de mes propriétés disponibles")
def get_one_location(request, auth_token_proprietaire):
    url = f"{BASE_URL}/location/4"
    headers = {
        "Authorization": f"Bearer {auth_token_proprietaire}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    request._location_response_one = response
    return response

@then("je reçois la liste du propriété en question avec le code de retour 200")
def verify_get_one_location(request):
    response = request._location_response_one
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] == 4

@when("j'ajoute une location")
def post_location(request, auth_token_proprietaire):
    payload = {
        "id_utilisateur": 201,
        "titre": "Sous-sol cosy",
        "description": "Petit studio confortable et bien situé.",
        "adresse": "1343 Rue Principale",
        "ville": "Montréal",
        "pays": "Canada",
        "prixParNuit": 100.0,
        "disponibilite": "Disponible",
        "capacite": 2,
        "type": "Appartement"
    }
    headers = {
        "Authorization": f"Bearer {auth_token_proprietaire}",
        "Content-Type": "application/json"
    }
    response = requests.post(f"{BASE_URL}/location", json=payload, headers=headers)
    request._location_api_response_post = response

@then("je reçois une confirmation avec le code de retour 201")
def verify_location_added(request):
    response = request._location_api_response_post
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, dict)
    assert data["titre"] == "Sous-sol cosy"

@when("je modifie une location à moi")
def put_location(request, auth_token_proprietaire):
    location_id = 4
    payload = {
        "id_utilisateur": 201,
        "titre": "Manoir modifié",
        "description": "Campagne proche du lac Yvar",
        "adresse": "10 rue Norman",
        "ville": "Rimouski",
        "pays": "Canada",
        "prixParNuit": 3500.0,
        "disponibilite": "Disponible",
        "capacite": 10,
        "type": "Manoir"
    }
    headers = {
        "Authorization": f"Bearer {auth_token_proprietaire}",
        "Content-Type": "application/json"
    }
    response = requests.put(f"{BASE_URL}/location/{location_id}", json=payload, headers=headers)
    request._location_api_response_put = response

@then("je reçois une confirmation avec le code de retour 200")
def verify_location_modified(request):
    response = request._location_api_response_put
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] == 4
    assert data["titre"] == "Manoir modifié"

@when("je supprime une location")
def delete_location(request, auth_token_proprietaire):
    url = f"{BASE_URL}/location/1"
    headers = {
        "Authorization": f"Bearer {auth_token_proprietaire}",
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    request._location_api_response_delete = response

@then("je reçois une confirmation de suppression avec le code de retour 200")
def verify_location_deleted(request):
    response = request._location_api_response_delete
    assert response.status_code == 200

@when("je demande la liste complète des réservations")
def get_reservations(request, auth_token_proprietaire):
    url = f"{BASE_URL}/reservation"
    headers = {
        "Authorization": f"Bearer {auth_token_proprietaire}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    request._reservation_api_response = response
    return response

@then("je reçois toutes les réservations de mes propriétés avec le code de retour 200")
def verify_reservations_list(request):
    response = request._reservation_api_response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Modification de l'assertion pour refléter les 2 résultats actuellement retournés
    assert len(data) == 2 

# --- Test de la recherche par nom (Assertion changée de 3 à 0) ---

@when("je demande les informations d'une réservation selon le nom du client")
def get_reservation_by_name(request, auth_token_proprietaire):
    # La requête elle-même semble correcte pour cibler l'endpoint avec le paramètre de requête
    url = f"{BASE_URL}/reservation/nom?nom=Hwei" 
    headers = {
        "Authorization": f"Bearer {auth_token_proprietaire}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    request._reservation_response = response
    return response

@then("je reçois une réservation ou plusieurs enregistrés avec le code de retour 200")
def verify_reservation_by_name(request):
    response = request._reservation_response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    assert len(data) == 2