from pydantic import BaseModel, Field

class PokemonValidationResponse(BaseModel):
    pokemon_name: str = Field(description="Nombre del Pokémon evaluado", examples=["pikachu"])
    profile_name: str = Field(description="Nombre del perfil contra el que se evaluó", examples=["fast_attacker"])
    is_valid: bool = Field(description="Indica si el Pokémon cumple con todos los requisitos del perfil")
    reason: str = Field(description="Motivo de la validación, ya sea éxito o la primera regla que falló") 