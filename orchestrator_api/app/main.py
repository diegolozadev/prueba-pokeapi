from fastapi import FastAPI
from app.api.endpoints import router as validator_router

app = FastAPI(title="Orchestrator API - PokeAPI Test")

# Registramos las rutas del validador
app.include_router(validator_router)

@app.get("/")
def read_root():
    return {"message": "Orchestrator API is running"}