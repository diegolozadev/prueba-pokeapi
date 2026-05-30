from fastapi import APIRouter
from app.schemas.pokemon import PokemonValidationResponse
from app.services.validator_service import validate_pokemon_against_profile

router = APIRouter(tags=["validation"])

@router.get(
    "/validate/{pokemon_name}/{profile_name}",
    response_model=PokemonValidationResponse,
    summary="Validar Pokémon contra un perfil",
    description="Evalúa si un Pokémon cumple con los requisitos mínimos de stats definidos en un perfil de contrato. Consulta la PokeAPI para obtener las stats y la Contract API para las reglas del perfil.",
    responses={
        404: {
            "description": "Pokémon o perfil no encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Pokemon 'pikachu' not found in PokeAPI"}
                }
            },
        },
        503: {
            "description": "Contract API fuera de servicio",
            "content": {
                "application/json": {
                    "example": {"detail": "Contract API is offline. Please start the contract server."}
                }
            },
        },
    },
)
async def validate_pokemon(pokemon_name: str, profile_name: str):
    result = await validate_pokemon_against_profile(pokemon_name, profile_name)
    return result