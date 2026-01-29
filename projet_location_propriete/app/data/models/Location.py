from enum import Enum
from pydantic import BaseModel

class Disponibilite(str, Enum):
    disponible = "Disponible"
    occupe = "Occupé"
    indisponible = "Indisponible"


class TypeLogement(str, Enum):
    appartement = "Appartement"
    chalet = "Chalet"
    maison = "Maison"
    loft = "Loft"
    manoir = "Manoir"

class Location(BaseModel):
    id: int
    id_utilisateur: int
    titre: str
    description: str
    adresse: str
    ville: str
    pays: str
    prixParNuit: float
    disponibilite: Disponibilite = Disponibilite.disponible
    capacite: int = 1
    type: TypeLogement