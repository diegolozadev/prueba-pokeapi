from fastapi import APIRouter, HTTPException, status
from app.schemas.profile import ProfileResponse
from app.services.profile_service import get_profile_by_name

router = APIRouter(tags=["profiles"])

@router.get(
    "/profiles/{name}",
    response_model=ProfileResponse,
    summary="Obtener perfil por nombre",
    description="Retorna un perfil de validación con sus reglas de stats mínimos para evaluar Pokémon.",
    responses={
        404: {
            "description": "Perfil no encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Profile not found"}
                }
            },
        },
    },
)
def read_profile(name: str):
    profile = get_profile_by_name(name)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile