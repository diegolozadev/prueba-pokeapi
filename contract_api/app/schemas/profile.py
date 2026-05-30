from pydantic import BaseModel 
from typing import Optional

class EvaluationRules(BaseModel):
    min_hp: int = 0
    min_attack: int = 0
    min_defense: int = 0
    min_speed: int = 0

class ProfileResponse(BaseModel):
    profile_name: str
    description: str
    rules: EvaluationRules