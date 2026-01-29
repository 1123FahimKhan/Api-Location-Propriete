import time
import mysql.connector
from mysql.connector import Error

def get_connection(retries=3, delay=3):
    for i in range(retries):
        try:
            connection = mysql.connector.connect(
                host="db",
                user="apiuser",
                password="apipassword",
                database="fkhan_locations"
            )
            print("Connexion MariaDB réussie")
            return connection
        except Error as e:
            print(f"Tentative {i+1}/{retries} - Erreur connexion MariaDB : {e}")
            time.sleep(delay)
    return None