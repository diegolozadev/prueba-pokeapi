from pydantic import BaseModel

# Este será el molde de la respuesta final que dará el Orquestador
class PokemonValidationResponse(BaseModel):
    pokemon_name: str
    profile_name: str
    is_valid: bool
    reason: str 