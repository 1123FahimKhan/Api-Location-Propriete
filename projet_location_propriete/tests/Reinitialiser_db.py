import requests
import pytest

BASE_URL = "http://localhost:10164/admin"

from pytest_bdd import scenarios, given, when, then

scenarios("../features/reset.feature")

#
#   Récit utilisateur - Tout le monde :
#   En tant qu'administrateur je veux avoir la liste complète des locations 
#

@given("Je suis un administrateur")
def user_administrateur():
    pass

@when("je veux reinitialiser la bd")
def reset_bd(request):
    url = f"{BASE_URL}/reset"
    response = requests.put(url)
    request._reset_api_response = response
    return response

@then("je reçois le code de retour 200")
def verify_reset(request):
    response = request._reset_api_response
    assert response.status_code == 200