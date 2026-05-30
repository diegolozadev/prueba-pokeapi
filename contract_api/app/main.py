from fastapi import FastAPI
from app.api.endpoints import router as profile_router

app = FastAPI(
    title="Contract API",
    description="API de contratos que define y expone perfiles de validación con reglas de stats mínimos para Pokémon.",
    version="1.0.0",
    contact={
        "name": "PokeAPI Test",
        "url": "https://pokeapi.co/",
    },
    docs_url="/docs",
    redoc_url=None,
)

app.include_router(profile_router)

@app.get("/")
def read_root():
    return {"message": "Contract API is running"}