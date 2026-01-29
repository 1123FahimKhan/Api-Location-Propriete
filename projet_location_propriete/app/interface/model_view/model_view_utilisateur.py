from pydantic import BaseModel, ConfigDict

class UtilisateursView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nom: str
    email: str