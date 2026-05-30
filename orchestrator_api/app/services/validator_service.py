from app.services.poke_service import get_pokemon_stats
from app.services.contract_service import get_profile_rules
from app.schemas.pokemon import PokemonValidationResponse

async def validate_pokemon_against_profile(pokemon_name: str, profile_name: str) -> PokemonValidationResponse:
    # 1. Traemos de forma asíncrona los stats del Pokémon desde la PokeAPI
    pokemon_stats = await get_pokemon_stats(pokemon_name)
    
    # 2. Traemos de forma asíncrona las reglas del perfil desde el Contract API
    profile_data = await get_profile_rules(profile_name)
    rules = profile_data["rules"]  # Extraemos el sub-diccionario de reglas
    
    # 3. Mapeamos los nombres de los stats de la PokeAPI a las llaves de nuestras reglas
    stats_to_check = [
        ("hp", "min_hp", "Vida"),
        ("attack", "min_attack", "Ataque"),
        ("defense", "min_defense", "Defensa"),
        ("speed", "min_speed", "Velocidad")
    ]
    
    # 4. Evaluamos regla por regla
    for poke_stat_name, rule_key, friendly_name in stats_to_check:
        actual_value = pokemon_stats.get(poke_stat_name, 0)
        required_value = rules.get(rule_key, 0)
        
        # Si el stat del Pokémon es menor al requerido por el contrato, rechaza de una
        if actual_value < required_value:
            return PokemonValidationResponse(
                pokemon_name=pokemon_name,
                profile_name=profile_name,
                is_valid=False,
                reason=f"Falló en {friendly_name}: Tiene {actual_value} y el mínimo requerido es {required_value}."
            )
            
    # 5. Si paso todo el bucle sin romperse, ¡el Pokémon es apto para el contrato!
    return PokemonValidationResponse(
        pokemon_name=pokemon_name,
        profile_name=profile_name,
        is_valid=True,
        reason="Validación exitosa. El Pokémon cumple con todos los requisitos del perfil."
    )