from fastapi import APIRouter
from app.schemas.pokemon import PokemonValidationResponse
from app.services.validator_service import validate_pokemon_against_profile

router = APIRouter()

# Definimos la ruta que recibirá el nombre del pokémon y el perfil a evaluar
@router.get("/validate/{pokemon_name}/{profile_name}", response_model=PokemonValidationResponse)
async def validate_pokemon(pokemon_name: str, profile_name: str):
    # Le pasamos el trabajo al validador maestro
    result = await validate_pokemon_against_profile(pokemon_name, profile_name)
    return result