from fastapi import FastAPI
# Importamos el enrutador de endpoints
from app.api.endpoints import router as profile_router

app = FastAPI(title="Contract API - PokeAPI Test")

# FastAPI que registra las rutas de los perfiles
app.include_router(profile_router)

@app.get("/")
def read_root():
    return {"message": "Contract API is running"}