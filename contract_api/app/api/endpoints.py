from fastapi import APIRouter, HTTPException
from app.schemas.profile import ProfileResponse
from app.services.profile_service import get_profile_by_name

# Creamos el enrutador que agrupa las rutas de perfiles
router = APIRouter()

@router.get("/profiles/{name}", response_model=ProfileResponse)
def read_profile(name: str):
    # Llevamos el nombre al servicio para que busque en la base de datos
    profile = get_profile_by_name(name)
    
    # Si el servicio nos devolvió None, disparamos un error 404 (No encontrado)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    # Si todo está bien, devolvemos el perfil que encontramos
    return profile