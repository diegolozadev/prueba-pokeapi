from app.schemas.profile import ProfileResponse

PROFILES_DB = {
    "fast_attacker": {
        "profile_name": "fast_attacker",
        "description": "Perfil diseñado para Pokémon con alto ataque y velocidad.",
        "rules": {
            "min_attack": 80,
            "min_speed": 90
        }
    }
}

def get_profile_by_name(name: str):
    # Buscamos el perfil usando su nombre como llave
    profile = PROFILES_DB.get(name)
    
    # Si no existe en el diccionario, devolvemos None
    if not profile:
        return None
        
    # Si existe, lo devolvemos
    return ProfileResponse(
        profile_name=profile["profile_name"],
        description=profile["description"],
        rules=profile["rules"]
    )