from pydantic import BaseModel

class Utilisateur(BaseModel):
    id: int
    nom: str
    email: str