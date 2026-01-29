Feature: Locations
    Un api de gestion des location de propriété

    Scenario: Gestion des locations de proriété
        Given Je suis un client
        When Je demande la liste des proriétés disponibles
        Then Je reçois 20 proriétés enregistrés avec le code de retour 200

    Scenario: Obtenir une location en particulier
        Given Je suis un client
        When Je demande les informations d'une proriété via son id
        Then Je reçois une proriété enregistré avec le code de retour 200