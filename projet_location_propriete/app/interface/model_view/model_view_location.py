from enum import Enum
from pydantic import BaseModel, ConfigDict
from app.data.models.Location import Disponibilite, TypeLogement

class LocationView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_utilisateur: int
    titre: str
    DESCRIPTION: str
    adresse: str
    ville: str
    pays: str
    prixParNuit: float
    disponibilite: Disponibilite = Disponibilite.disponible
    capacite: int = 1
    type: TypeLogement