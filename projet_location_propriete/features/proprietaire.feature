Feature: Proprietaire
    Un api de gestion des location de propriété selon le proprietaire


Scenario: Le propriétaire obtient la liste de ses locations
    Given je suis un proprietaire
    When je demande la liste de mes propriétés disponibles
    Then je reçois la liste de tous mes propriété avec le code de retour 200

Scenario: Le propriétaire obtient une location par son identifiant
    Given je suis un proprietaire
    When je demande dans la liste seulement un de mes propriétés disponibles
    Then je reçois la liste du propriété en question avec le code de retour 200

Scenario: Le propriétaire ajoute une location
    Given je suis un proprietaire
    When j'ajoute une location
    Then je reçois une confirmation avec le code de retour 201

Scenario: Le propriétaire modifie une location
    Given je suis un proprietaire
    When je modifie une location à moi
    Then je reçois une confirmation avec le code de retour 200

Scenario: Le propriétaire supprime une location
    Given je suis un proprietaire
    When je supprime une location
    Then je reçois une confirmation de suppression avec le code de retour 200

Scenario: Gestion des réservations des propriétés
    Given je suis un proprietaire
    When je demande la liste complète des réservations
    Then je reçois toutes les réservations de mes propriétés avec le code de retour 200

Scenario: Obtenir une réservation en particulier
    Given je suis un proprietaire
    When je demande les informations d'une réservation selon le nom du client
    Then je reçois une réservation ou plusieurs enregistrés avec le code de retour 200
