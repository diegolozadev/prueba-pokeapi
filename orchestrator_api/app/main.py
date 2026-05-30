from fastapi import FastAPI
from app.api.endpoints import router as validator_router

app = FastAPI(
    title="Orchestrator API",
    description="API de orquestación que valida Pokémon contra perfiles de contrato. Consulta la PokeAPI para obtener stats y la Contract API para las reglas.",
    version="1.0.0",
    contact={
        "name": "PokeAPI Test",
        "url": "https://pokeapi.co/",
    },
    docs_url="/docs",
    redoc_url=None,
)

app.include_router(validator_router)

@app.get("/")
def read_root():
    return {"message": "Orchestrator API is running"}