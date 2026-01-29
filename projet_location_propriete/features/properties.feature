Feature: Properties
    Un api de gestion des location de propriété

    Scenario: Gestion des locations de proriété
        Given Je suis un client
        When Je demande la liste des proriétés disponibles
        Then Je reçois 6 proriétés enregistrés avec le code de retour 200

    Scenario: Obtenir une location en particulier
        Given Je suis un propriétaire
        When Je demande les informations d'une proriété via son id
        Then Je reçois une proriété enregistré avec le code de retour 200

    Scenario: Propriétaire/admin modifie une location
        Given Je suis un propriétaire
        When Je modifie une location à moi
        Then Je reçois une confirmation avec le code de retour 200

    Scenario: Propriétaire/admin ajoute une location
        Given Je suis un propriétaire
        When J'ajoute une location
        Then Je reçois une confirmation avec le code de retour 201

    Scenario: Propriétaire/admin supprimer une location
        Given Je suis un propriétaire
        When Je supprime une location
        Then Je reçois une confirmation de suppression avec le code de retour 200
