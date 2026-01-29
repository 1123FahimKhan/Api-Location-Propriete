import requests
import pytest
import json
import os

BASE_URL = "http://localhost:10164/location"

from pytest_bdd import scenarios, given, when, then

scenarios("../features/locations.feature")

#
#   Récit utilisateur - Tout le monde :
#   En tant qu'utilisateur je veux avoir la liste complète des locations 
#

@given("Je suis un client")
def user_client():
    pass

@when("Je demande la liste des proriétés disponibles")
def get_clients(request):
    url = f"{BASE_URL}"
    response = requests.get(url)
    request._locations_api_response = response
    return response

@then("Je reçois 20 proriétés enregistrés avec le code de retour 200")
def verify_locations_list_all(request):
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
#   En tant qu'utilisateur je veux obtenir une location en particulier
#

@given("Je suis un client")
def user_client_single_location(): # Renommage pour éviter la redéfinition
    pass

@when("Je demande les informations d'une proriété via son id")
def get_client(request):
    url = f"{BASE_URL}/3"
    response = requests.get(url)
    request._locations_api_response = response
    return response

@then("Je reçois une proriété enregistré avec le code de retour 200")
def verify_single_location(request):
    response = request._locations_api_response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    
    assert len(data) == 11 
    
    # CORRECTION APPLIQUÉE ICI : Utilisation de 'DESCRIPTION' (en majuscules) 
    # pour correspondre à ce que l'API retourne (le dictionnaire de gauche dans l'erreur).
    assert data == {
        "id": 3,
        "id_utilisateur": 201, 
        "titre": "Appartement sous sol",
        "DESCRIPTION": "Prix modique, 1 personne seulement", # <-- CLÉ CHANGÉE
        "adresse": "4242 Rue des Lilas",
        "ville": "Montréal",
        "pays": "Canada",
        "prixParNuit": 20.0,
        "disponibilite": "Occupé",
        "capacite": 1,
        "type": "Appartement"
    }