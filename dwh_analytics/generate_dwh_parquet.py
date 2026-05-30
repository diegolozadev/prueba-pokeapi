import os
import pandas as pd
import requests

# Configuración inicial
os.makedirs("data", exist_ok=True)
BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
TOTAL_POKEMON = 151  # Primera generación completa

print(f"🚀 Iniciando proceso ETL para extraer los {TOTAL_POKEMON} Pokémon originales...")

# Diccionarios globales para mapear nombres de entidades a sus Surrogate Keys (IDs únicos del DWH)
types_map = {}
abilities_map = {}
moves_map = {}

# Listas donde acumularemos los registros para cada tabla
fact_stats_rows = []
rel_types_rows = []
rel_abilities_rows = []
rel_moves_rows = []

# --- EXTRACT & TRANSFORM ---
for i in range(1, TOTAL_POKEMON + 1):
    print(f"📥 Extrayendo datos de: #{i}...", end="\r")
    try:
        response = requests.get(f"{BASE_URL}{i}", timeout=10)
        if response.status_code != 200:
            continue
        data = response.json()
        
        # 1. Extraer metadata básica y Stats (Para la Tabla de Hechos)
        pokemon_id = data["id"]
        nombre = data["name"].capitalize()
        
        # Mapeamos los stats convirtiendo la lista de la API a un diccionario limpio
        stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
        
        # Guardamos la fila para fact_pokemon_stats (Usamos el id_pokemon como sk_pokemon en este caso)
        fact_stats_rows.append({
            "sk_pokemon": pokemon_id,
            "id_pokemon": pokemon_id,
            "nombre": nombre,
            "hp": stats.get("hp", 0),
            "attack": stats.get("attack", 0),
            "defense": stats.get("defense", 0),
            "special_attack": stats.get("special-attack", 0),
            "special_defense": stats.get("special-defense", 0),
            "speed": stats.get("speed", 0)
        })
        
        # 2. Procesar TIPOS (dim_types y rel_pokemon_types)
        for t in data["types"]:
            type_name = t["type"]["name"].capitalize()
            slot = t["slot"]
            
            # Si el tipo no está mapeado en la dimensión, le asignamos una nueva SK numérica
            if type_name not in types_map:
                types_map[type_name] = len(types_map) + 1
                
            rel_types_rows.append({
                "sk_pokemon": pokemon_id,
                "sk_type": types_map[type_name],
                "slot": slot
            })
            
        # 3. Procesar HABILIDADES (dim_abilities y rel_pokemon_abilities)
        for a in data["abilities"]:
            ability_name = a["ability"]["name"].replace("-", " ").title()
            is_hidden = a["is_hidden"]
            
            if ability_name not in abilities_map:
                abilities_map[ability_name] = len(abilities_map) + 1
                
            rel_abilities_rows.append({
                "sk_pokemon": pokemon_id,
                "sk_ability": abilities_map[ability_name],
                "is_hidden": is_hidden
            })
            
        # 4. Procesar MOVIMIENTOS (dim_moves y rel_pokemon_moves)
        for m in data["moves"]:
            move_name = m["move"]["name"].replace("-", " ").title()
            
            if move_name not in moves_map:
                moves_map[move_name] = len(moves_map) + 1
                
            rel_moves_rows.append({
                "sk_pokemon": pokemon_id,
                "sk_move": moves_map[move_name]
            })
            
    except Exception as e:
        print(f"\n❌ Error procesando el Pokémon #{i}: {e}")

print("\n\n🔄 Estructurando DataFrames y exportando a Parquet...")

# --- LOAD (Crear los archivos Parquet definitivos) ---

# Tablas Maestras (Dimensiones) construidas dinámicamente a partir del mapa de llaves
df_dim_types = pd.DataFrame([{"sk_type": v, "type_name": k} for k, v in types_map.items()])
df_dim_abilities = pd.DataFrame([{"sk_ability": v, "ability_name": k} for k, v in abilities_map.items()])
df_dim_moves = pd.DataFrame([{"sk_move": v, "move_name": k} for k, v in moves_map.items()])

# Tablas de Hechos y Tablas Relacionales (Puente)
df_fact_pokemon_stats = pd.DataFrame(fact_stats_rows)
df_rel_pokemon_types = pd.DataFrame(rel_types_rows)
df_rel_pokemon_abilities = pd.DataFrame(rel_abilities_rows)
df_rel_pokemon_moves = pd.DataFrame(rel_moves_rows)

# Guardar todo en formato .parquet de forma local
df_dim_types.to_parquet("data/dim_types.parquet", index=False)
df_dim_abilities.to_parquet("data/dim_abilities.parquet", index=False)
df_dim_moves.to_parquet("data/dim_moves.parquet", index=False)
df_fact_pokemon_stats.to_parquet("data/fact_pokemon_stats.parquet", index=False)
df_rel_pokemon_types.to_parquet("data/rel_pokemon_types.parquet", index=False)
df_rel_pokemon_abilities.to_parquet("data/rel_pokemon_abilities.parquet", index=False)
df_rel_pokemon_moves.to_parquet("data/rel_pokemon_moves.parquet", index=False)

print("---")
print(f"✅ ¡ETL Finalizado con éxito!")
print(f"📊 Resumen de registros cargados:")
print(f"   - dim_types.parquet: {len(df_dim_types)} registros")
print(f"   - dim_abilities.parquet: {len(df_dim_abilities)} registros")
print(f"   - dim_moves.parquet: {len(df_dim_moves)} registros")
print(f"   - fact_pokemon_stats.parquet: {len(df_fact_pokemon_stats)} registros (Los 151 Pokémon)")
print(f"   - rel_pokemon_types.parquet: {len(df_rel_pokemon_types)} registros")
print(f"   - rel_pokemon_abilities.parquet: {len(df_rel_pokemon_abilities)} registros")
print(f"   - rel_pokemon_moves.parquet: {len(df_rel_pokemon_moves)} registros")