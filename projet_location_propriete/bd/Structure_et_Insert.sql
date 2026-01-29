CREATE DATABASE IF NOT EXISTS fkhan_locations;
USE fkhan_locations;
DROP TABLE IF EXISTS Paiement;
DROP TABLE IF EXISTS Reservation;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS Proprietaire;
DROP TABLE IF EXISTS Utilisateur;

CREATE TABLE Utilisateur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'proprietaire', 'client') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Proprietaire (
    id INT PRIMARY KEY,
    nom VARCHAR(100),
    CONSTRAINT fk_proprietaire_utilisateur
        FOREIGN KEY (id) REFERENCES Utilisateur(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Client (
    id INT PRIMARY KEY,
    nom VARCHAR(100),
    CONSTRAINT fk_client_utilisateur
        FOREIGN KEY (id) REFERENCES Utilisateur(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Location (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    titre VARCHAR(255) NOT NULL,
    DESCRIPTION TEXT,
    adresse VARCHAR(255),
    ville VARCHAR(100),
    pays VARCHAR(100),
    prixParNuit DECIMAL(10,2) NOT NULL,
    disponibilite ENUM('Disponible', 'Occupé', 'Indisponible') DEFAULT 'Disponible',
    capacite INT CHECK (capacite >= 1),
    type ENUM('Appartement', 'Chalet', 'Maison', 'Loft', 'Manoir') NOT NULL,
    CONSTRAINT fk_location_utilisateur
        FOREIGN KEY (id_utilisateur)
        REFERENCES Utilisateur(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_debut DATE,
    date_fin DATE,
    statut VARCHAR(50),
    montant_total FLOAT,
    client_id INT,
    location_id INT,
    CONSTRAINT fk_reservation_client
        FOREIGN KEY (client_id) REFERENCES Client(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_reservation_location
        FOREIGN KEY (location_id) REFERENCES Location(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Paiement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    montant FLOAT,
    date_paiement DATE,
    moyen_paiement VARCHAR(50),
    reservation_id INT,
    CONSTRAINT fk_paiement_reservation
        FOREIGN KEY (reservation_id) REFERENCES Reservation(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO Utilisateur (id, nom, username, email, hashed_password, role) VALUES
(103, 'Hwei', 'hwei', 'hwei.c@email.com', 'HASH_A_REMPLACER_HWEI', 'client'),
(201, 'Mike', 'mike', 'mike.p@email.com', 'HASH_A_REMPLACER_MIKE', 'proprietaire'),
(301, 'Admin Joe', 'adminjoe', 'admin.joe@email.com', 'HASH_A_REMPLACER_ADMIN', 'admin'),
(400, 'Mat', 'mat', 'mathematique101@mat.com', 'HASH_A_REMPLACER_MAT', 'proprietaire');

INSERT INTO Proprietaire (id, nom) VALUES
(201, 'Mike'),
(400, 'Mat');

INSERT INTO Client (id, nom) VALUES
(103, 'Hwei');

INSERT INTO Location (id, id_utilisateur, titre, DESCRIPTION, adresse, ville, pays, prixParNuit, disponibilite, capacite, type) VALUES
(1, 201, 'Appartement cosy', 'Proche du centre-ville', '123 Rue Principale', 'Montréal', 'Canada', 85, 'Disponible', 2, 'Appartement'),
(2, 201, 'Chalet au bord du lac', 'Vue magnifique sur le lac', '45 Chemin du Lac', 'Québec', 'Canada', 150, 'Disponible', 6, 'Chalet'),
(3, 201, 'Appartement sous sol', 'Prix modique, 1 personne seulement', '4242 Rue des Lilas', 'Montréal', 'Canada', 20, 'Occupé', 1, 'Appartement'),
(4, 201, 'Manoir de George Vernon', 'Campagne proche du lac Yvar', '10 rue norman', 'Rimouski', 'Canada', 3500, 'Disponible', 10, 'Manoir'),
(5, 201, 'Maison en pierre', 'En plein milieu d''une forêt et un joli cours d''eau', '4 rand no.8', 'Lac-du-milieu', 'Canada', 320, 'Disponible', 4, 'Maison'),
(6, 201, 'Loft moderne', 'Avec terrasse et belle vue', '77 Rue Sainte-Catherine', 'Montréal', 'Canada', 120, 'Disponible', 3, 'Loft');

INSERT INTO Reservation (id, date_debut, date_fin, statut, montant_total, client_id, location_id) VALUES
(10, '2025-12-01', '2025-12-05', 'Confirmée', 400.00, 103, 1),
(11, '2026-01-10', '2026-01-12', 'Confirmée', 500.00, 103, 2),
(12, '2025-11-20', '2025-11-22', 'En attente de paiement', 360.00, 103, 4);

INSERT INTO Paiement (id, montant, date_paiement, moyen_paiement, reservation_id) VALUES
(100, 400.00, '2025-10-15', 'Carte Bancaire', 10),
(101, 500.00, '2025-10-20', 'PayPal', 11);

ALTER TABLE Location RENAME COLUMN id_utilisateur to id_utilisateur;

USE locations;

DESCRIBE Location;

DESCRIBE Utilisateur;

SELECT * FROM Location;

SELECT * FROM Location WHERE id = 3;

SELECT * FROM Client;

SELECT * FROM Reservation;

SELECT * FROM Utilisateur;

SELECT *
FROM Reservation
RIGHT JOIN Client ON Reservation.client_id = Client.id
WHERE Client.nom = "Hwei";


SELECT Location.*, Reservation.*
FROM Location
LEFT JOIN Reservation ON Location.id_utilisateur = Reservation.client_id

UNION

SELECT Location.*, Reservation.*
FROM Location
RIGHT JOIN Reservation ON Location.id_utilisateur = Reservation.client_id;

INSERT INTO Location (id_utilisateur, titre, description, adresse, ville, pays, prixParNuit, disponibilite, capacite, type) 
VALUES (201, 'Maison hanté', 'berceuse qui bouge', '666 Rue Macabre', 'Québec', 'Canada', 100.2, 'Disponible', 3, 'Maison');

drop table Location;
