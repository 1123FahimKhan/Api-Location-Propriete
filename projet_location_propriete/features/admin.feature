Feature: Admin
    Un api de gestion des location de propriété selon l'admin

    Scenario: Gestion des locations de proriétés
        Given Je suis un administrateur
        When Je demande la liste complète des proriétés
        Then Je reçois 6 proriétés enregistrés avec le code de retour 200

    Scenario: Obtenir une location en particulier
        Given Je suis un administrateur
        When Je demande les informations d'une proriété via son id
        Then Je reçois une proriété enregistré avec le code de retour 200

    Scenario: Gestion des utilisateurs
        Given Je suis un administrateur
        When Je demande la liste complète des utilisateurs
        Then Je reçois 3 utilisateurs enregistrés avec le code de retour 200

    Scenario: Obtenir un utilisateur en particulier
        Given Je suis un administrateur
        When Je demande les informations d'un utilisateur via son id
        Then Je reçois un utilisateur enregistré avec le code de retour 200

    Scenario: Gestion des réservations de proriétés
        Given Je suis un administrateur
        When Je demande la liste complète des réservations
        Then Je reçois 3 réservations enregistrés avec le code de retour 200

    Scenario: Obtenir une réservation en particulier
        Given Je suis un administrateur
        When Je demande les informations d'une réservation selon le nom du client
        Then Je reçois une réservation ou plusieurs enregistrés avec le code de retour 200

    Scenario: Ajouter une location
        Given Je suis un administrateur
        When Je veux ajouter une location pour un propriétaire
        Then Je reçois une confirmation d'ajout location avec le code de retour 201

    Scenario: Ajouter un utilisateur
        Given Je suis un administrateur
        When Je veux ajouter un utilisateur
        Then Je reçois une confirmation d'ajout utilisateur avec le code de retour 201

    Scenario: Ajouter une réservation
        Given Je suis un administrateur
        When Je veux ajouter une reservation pour un client
        Then Je reçois une confirmation d'ajout reservation avec le code de retour 201
        
    Scenario: Modifier une location
        Given Je suis un administrateur
        When je modifie une location
        Then je reçois une confirmation de modification de location avec le code de retour 200

    Scenario: Modifier un utilisateur
        Given Je suis un administrateur
        When je modifie un utilisateur
        Then je reçois une confirmation de modification de utilisateur avec le code de retour 200

    Scenario: Modifier une réservation
        Given Je suis un administrateur
        When je modifie une reservation
        Then je reçois une confirmation de modification de reservation avec le code de retour 200

    Scenario: Supprimer une location
        Given Je suis un administrateur
        When je supprime une location
        Then je reçois une confirmation de suppression location avec le code de retour 200

    Scenario: Supprimer un utilisateur
        Given Je suis un administrateur
        When je supprime un utilisateur
        Then je reçois une confirmation de suppression utilisateur avec le code de retour 200

    Scenario: Supprimer une réservation
        Given Je suis un administrateur
        When je supprime une reservation
        Then je reçois une confirmation de suppression reservation avec le code de retour 200