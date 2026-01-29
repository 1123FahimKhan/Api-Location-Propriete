Feature: Admin
    Réinitialiser la base donnée pour utilité des tests

    
    Scenario: Réinitialiser la bd
        Given Je suis un administrateur
        When je veux reinitialiser la bd
        Then je reçois le code de retour 200