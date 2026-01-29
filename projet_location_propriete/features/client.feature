Feature: Client
    Un api de gestion des location de propriété selon le client


Scenario: Le client obtient la liste de ses locations
    Given je suis un client
    When je demande la liste de mes propriétés disponibles
    Then je reçois la liste de tous mes propriété avec le code de retour 200

Scenario: Le client obtient une location par son identifiant
    Given je suis un client
    When je demande dans la liste seulement un de mes propriétés disponibles
    Then je reçois la liste du propriété en question avec le code de retour 200

Scenario: Le client ajoute une location
    Given je suis un client
    When j'ajoute une location à louer
    Then je reçois une confirmation avec le code de retour 201

Scenario: Gestion des réservations des propriétés
    Given je suis un client
    When je demande la liste complète de mes réservations
    Then je reçois toutes les réservations de mes propriétés réservavec le code de retour 200
