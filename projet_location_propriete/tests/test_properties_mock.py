import requests
import pytest
import json
import os

BASE_URL = "https://80492394-7056-4f7a-94e0-6d65978c7a64.mock.pstmn.io"

from pytest_bdd import scenarios, given, when, then

scenarios("../features/properties.feature")

#
#   Récit utilisateur - Tout le monde :
#   En tant qu'utilisateur je veux avoir la liste complète des propriétés 
#

@given("Je suis un client")
def user_client():
    pass

@when("Je demande la liste des proriétés disponibles")
def get_clients(request):
    url = f"{BASE_URL}/location"
    response = requests.get(url)
    request._locations_api_response = response
    return response

@then("Je reçois 6 proriétés enregistrés avec le code de retour 200")
def verify_locations_list(request):
    response = request._locations_api_response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    # Comparer la longueur
    assert len(data) == 6
    
    # Comparer le contenu json
    json_path = os.path.join(os.path.dirname(__file__), "listeLocation.json")
    with open(json_path, "r", encoding="utf-8") as f:
        expected_data = json.load(f)
    assert [d["titre"] for d in data] == [d["titre"] for d in expected_data]

#
#   Récit utilisateur - Tout le monde :
#   En tant qu'administrateur je veux avoir une propriété en particulier
#

@given("Je suis un propriétaire")
def user_client():
    pass

@when("Je demande les informations d'une proriété via son id")
def get_clients(request):
    url = f"{BASE_URL}/location/2"
    response = requests.get(url)
    request._locations_api_response = response
    return response

@then("Je reçois une proriété enregistré avec le code de retour 200")
def verify_locations_list(request):
    response = request._locations_api_response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data == {
        "id": 2,
        "id_utilisateur": 12,
        "titre": "Chalet au bord du lac",
        "description": "Vue magnifique sur le lac",
        "adresse": "45 Chemin du Lac",
        "ville": "Québec",
        "pays": "Canada",
        "prixParNuit": 150,
        "disponibilite": "Disponible",
        "capacite": 6,
        "type": "Chalet"
    }
    



#
#   Récit utilisateur - Propriétaires ou admin :
#   En tant que propriétaire/admin inscrit et connecté, 
#   je veux modifier une location,
#   afin de mettre à jour les informations de location 
#   
#   Propriétaire : Monti (id : 12)

@given("Je suis un propriétaire")
def user_proprietaire():
    pass

@when("Je modifie une location à moi")
def put_location(request):
    url = f"{BASE_URL}/location/6"
    payload = {
        "id_utilisateur": 12,
        "titre": "Loft moderne",
        "description": "Avec terrasse et belle vue",
        "adresse": "77 Rue Sainte-Catherine",
        "ville": "Montréal",
        "pays": "Canada",
        "prixParNuit": 120,
        "disponibilite": "Disponible",
        "capacite": 3,
        "type": "Loft"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.put(url, json=payload, headers=headers)
    request._locations_api_response_put = response
    return response

@then("Je reçois une confirmation avec le code de retour 200")
def verify_location_Mike(request):
    response = request._locations_api_response_put
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data['ville'] == "Montréal"

#
#   Récit utilisateur - Propriétaires ou admin :
#   En tant que propriétaire/admin inscrit et connecté, 
#   je veux ajouter une location,
#   afin de mettre une propriété en location 
#   

@given("Je suis un propriétaire")
def user_admin():
    pass

@when("J'ajoute une location")
def post_location(request):
    url = f"{BASE_URL}/location"
    payload = {
        "id_utilisateur": 3,
        "titre": "Loft moderne",
        "description": "Avec terrasse et belle vue",
        "adresse": "77 Rue Sainte-Catherine",
        "ville": "Montréal",
        "pays": "Canada",
        "prixParNuit": 250,
        "disponibilite": "Disponible",
        "capacite": 3,
        "type": "Loft"
    }
    response = requests.post(url, json=payload)
    request._locations_api_response_post = response
    return response

@then("Je reçois une confirmation avec le code de retour 201")
def verify_location_Joe(request):
    response = request._locations_api_response_post
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, dict)
    assert data == {
        "id": 8,
        "id_utilisateur": 3,
        "titre": "Loft moderne",
        "description": "Avec terrasse et belle vue",
        "adresse": "77 Rue Sainte-Catherine",
        "ville": "Montréal",
        "pays": "Canada",
        "prixParNuit": 250,
        "disponibilite": "Disponible",
        "capacite": 3,
        "type": "Loft"
    }

#
#   Récit utilisateur - Propriétaires ou admin :
#   En tant que propriétaire/admin inscrit et connecté, 
#   je veux supprimer une location,
#   afin de mettre fin à la location d'une propriété de manière permanent 
#   

@pytest.fixture
def delete_location_response():
    url = f"{BASE_URL}/location/2"
    response = requests.delete(url)
    assert response.status_code == 200
    return response

@given("Je suis un propriétaire")
def user_proprietaire():
    pass

@when("Je supprime une location")
def delete_location(delete_location_response):
    return delete_location_response

@then("Je reçois une confirmation de suppression avec le code de retour 200")
def verify_location_Monti(delete_location_response):
    assert delete_location_response.status_code == 200
    data = delete_location_response.json()
    assert isinstance(data, dict)
    assert len(data) == 0
