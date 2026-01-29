from fastapi import APIRouter, HTTPException
from app.interface.model_view.model_view_location import LocationView
from app.services import service_locations

router = APIRouter(prefix="/location", tags=["location"])

"""
Paramètre(s) : null
Valeur(s) de retour : La liste de toutes les locations disponibles.
    JSON : [
        {
            id: int
            id_utilisateur: int
            titre: str
            description: str
            adresse: str
            ville: str
            pays: str
            prixParNuit: float
            disponibilite: str
            capacite: int
            type: str
        }
    ]
    code de retour : 200
"""
@router.get("/", response_model=list[LocationView])
def get_locations():
    try:
        return service_locations.lister_locations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""
Paramètre(s) : id (int)
Valeur(s) de retour : La location correspondant à l'id fourni.
    JSON : {
        id: int
        id_utilisateur: int
        titre: str
        description: str
        adresse: str
        ville: str
        pays: str
        prixParNuit: float
        disponibilite: str
        capacite: int
        type: str
    }
    code de retour : 200
"""
@router.get("/{id}", response_model=LocationView)
def get_location_id(id: int):
    try:
        return service_locations.obtenir_location_avec_id(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
