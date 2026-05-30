from pydantic import BaseModel, Field

class EvaluationRules(BaseModel):
    min_hp: int = Field(default=0, description="Vida mínima requerida", examples=[80])
    min_attack: int = Field(default=0, description="Ataque mínimo requerido", examples=[80])
    min_defense: int = Field(default=0, description="Defensa mínima requerida", examples=[60])
    min_speed: int = Field(default=0, description="Velocidad mínima requerida", examples=[90])

class ProfileResponse(BaseModel):
    profile_name: str = Field(description="Nombre único del perfil", examples=["fast_attacker"])
    description: str = Field(description="Descripción del propósito del perfil")
    rules: EvaluationRules = Field(description="Reglas de stats mínimos que debe cumplir un Pokémon")