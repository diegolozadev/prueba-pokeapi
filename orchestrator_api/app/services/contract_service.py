import httpx
from fastapi import HTTPException

# URL de  la otra API (Contract API). 
# Puerto donde corre lo de contratos (usualmente 8000)
CONTRACT_API_URL = "http://127.0.0.1:8000/profiles/"

async def get_profile_rules(profile_name: str) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CONTRACT_API_URL}{profile_name}")
            
            # Si el perfil no existe en el Contract API, manejamos el 404
            if response.status_code == 404:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Profile '{profile_name}' not found in Contract API"
                )
                
            response.raise_for_status()
            
            # Si todo está bien, retornamos el JSON con las reglas del perfil
            return response.json()
            
        except httpx.ConnectError:
            # Este error salta si no se enciende la Contract API en la otra terminal
            raise HTTPException(
                status_code=503, 
                detail="Contract API is offline. Please start the contract server."
            )
        except httpx.HTTPStatusError:
            raise HTTPException(
                status_code=response.status_code, 
                detail="Error communicating with Contract API"
            )