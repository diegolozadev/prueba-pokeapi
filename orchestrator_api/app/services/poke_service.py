import httpx
from fastapi import HTTPException

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

async def get_pokemon_stats(pokemon_name: str) -> dict:
    # Usamos httpx.AsyncClient para hacer la petición de forma eficiente
    async with httpx.AsyncClient() as client:
        try:
            # Pasamos el nombre a minúsculas para evitar errores (ej. "Pikachu" -> "pikachu")
            response = await client.get(f"{POKEAPI_URL}{pokemon_name.lower()}")
            
            # Si el Pokémon no existe en la PokeAPI (devuelve 404), manejamos el error
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Pokemon '{pokemon_name}' not found in PokeAPI")
                
            # Si pasa otra cosa rara (error 500, etc.), levantamos el error
            response.raise_for_status()
            
            # Si todo sale bien, convertimos la respuesta a un diccionario de Python
            data = response.json()
            
            # De todo el montón de datos que da la PokeAPI, solo nos interesan los stats
            # Extraemos en un formato limpio y fácil de leer
            stats = {}
            for stat in data["stats"]:
                stat_name = stat["stat"]["name"]      # ej: "hp", "attack"
                base_stat = stat["base_stat"]         # ej: 35, 55
                stats[stat_name] = base_stat
                
            return stats
            
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=response.status_code, detail="Error communicating with PokeAPI")