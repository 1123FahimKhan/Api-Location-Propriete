import requests
import pytest
from pytest_bdd import scenarios, given, when, then
import json
from requests.exceptions import ConnectionError

BASE_URL = "http://localhost:10164/client" 
Login_URL = "http://localhost:10164/users/login"

scenarios("../features/client.feature")

def login(username, password):
    login_data = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(Login_URL, data=login_data)
    except ConnectionError as e:
        pytest.fail(f"ÉCHEC DE CONNEXION: Assurez-vous que l'API est démarrée sur {Login_URL}. Erreur: {e}")
    
    if response.status_code == 200:
        response_json = response.json()
        token = response_json.get("access_token")
        if token is None:
            pytest.fail(f"Connexion réussie (200) mais jeton manquant dans la réponse: {response.text}")
        return token
    else:
        pytest.fail(f"Échec de la connexion pour {username}. Code: {response.status_code}, Réponse: {response.text}")

@pytest.fixture(scope="session")
def auth_token_client():
    token = login("hwei", "hwei@2025")
    return token

@pytest.fixture
@given("je suis un client")
def user_client(auth_token_client):
    return auth_token_client

# --- 1. Lister les locations (Client/Propriétaire) ---

@when("je demande la liste de mes propriétés disponibles")
def get_locations(request, user_client):
    url = f"{BASE_URL}/location"
    headers = {
        "Authorization": f"Bearer {user_client}",
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
    if data:
        request.location_id_to_test = data[0]['id']
    else:
        request.location_id_to_test = 1

# --- 2. Obtenir une location par son identifiant ---

@when("je demande dans la liste seulement un de mes propriétés disponibles")
def get_one_location(request, user_client):
    location_id = getattr(request, 'location_id_to_test', 1)
    url = f"{BASE_URL}/location/{location_id}"
    headers = {
        "Authorization": f"Bearer {user_client}",
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
    assert data["id"] == getattr(request, 'location_id_to_test', 1)

# --- 3. Le client ajoute une location ---

@when("j'ajoute une location à louer")
def post_location(request, user_client):
    payload = {
        "id_utilisateur": 201, 
        "titre": "Location Ajoutée Client Test",
        "description": "Location créée par le client.",
        "adresse": "123 Rue Client",
        "ville": "Clientville",
        "pays": "Testland",
        "prixParNuit": 50.0,
        "disponibilite": "Disponible",
        "capacite": 1,
        "type": "Studio"
    }
    headers = {
        "Authorization": f"Bearer {user_client}",
        "Content-Type": "application/json"
    }
    response = requests.post(f"{BASE_URL}/location", json=payload, headers=headers)
    request._location_api_response_post = response

@then("je reçois une confirmation avec le code de retour 201")
def verify_location_added(request):
    response = request._location_api_response_post
    assert response.status_code == 201
    assert isinstance(response.json(), dict)

# --- 4. Gestion des réservations des propriétés ---

@when("je demande la liste complète de mes réservations")
def get_reservations(request, user_client):
    url = f"{BASE_URL}/reservation"
    headers = {
        "Authorization": f"Bearer {user_client}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    request._reservation_api_response = response
    return response

@then("je reçois toutes les réservations de mes propriétés réservavec le code de retour 200")
def verify_reservations_list(request):
    response = request._reservation_api_response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data is not None