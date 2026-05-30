# Prueba Técnica - PokeAPI Architecture & Analytics

Monorepo que implementa una arquitectura de microservicios alrededor de la [PokeAPI](https://pokeapi.co/), compuesta por dos APIs (Contract API y Orchestrator API) y un módulo de Data Warehouse analítico con modelo dimensional Snowflake.

---

## Arquitectura General

```
                     ┌──────────────────────────────────────────────┐
                     │              Orchestrator API               │
                     │         (FastAPI - puerto 8001)             │
                     │                                              │
                     │  GET /validate/{pokemon}/{profile}           │
                     │        │                           │         │
                     │        ▼                         ▼          │
                     │  poke_service            contract_service    │
                     │  (consume PokeAPI)     (consume Contract)    │
                     │        │                           │         │
                     └────────┼───────────────────────────┼─────────┘
                              │                           │
                              ▼                           ▼
                     ┌──────────────┐          ┌──────────────────────┐
                     │   PokeAPI    │          │    Contract API      │
                     │ (externa)    │          │ (FastAPI - puerto    │
                     │              │          │       8000)          │
                     │ pokemon/     │          │                      │
                     │   {name}     │          │ GET /profiles/{name} │
                     └──────────────┘          └──────────────────────┘

                     ┌──────────────────────────────────────────────┐
                     │              dwh_analytics/                  │
                     │   (independiente, no es un servicio HTTP)    │
                     │                                              │
                     │  generate_dwh_parquet.py                     │
                     │       │                                      │
                     │       ▼ (consume PokeAPI directamente)       │
                     │  PokeAPI                                     │
                     │       │                                      │
                     │       ▼                                      │
                     │  DataFrames → archivos .parquet              │
                     │  + consultas SQL analíticas                  │
                     └──────────────────────────────────────────────┘
```

### Flujo de validación

1. El cliente llama a `GET /validate/{pokemon_name}/{profile_name}` en el Orchestrator API.
2. El Orchestrator consulta la **PokeAPI** para obtener las stats base del Pokémon.
3. Simultáneamente consulta la **Contract API** para obtener las reglas del perfil solicitado.
4. Compara cada stat contra el mínimo exigido por el perfil.
5. Retorna `is_valid: true/false` con el motivo.

---

## Orchestrator API

API principal que orquesta la validación de Pokémon contra perfiles de contrato.

### Setup

```bash
cd orchestrator_api
pip install -r ..\requirements.txt
uvicorn app.main:app --reload --port 8001
```

### Endpoint

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/validate/{pokemon_name}/{profile_name}` | Valida un Pokémon contra un perfil |

#### Ejemplo

```bash
# Solicitud
curl "http://localhost:8001/validate/pikachu/fast_attacker"

# Respuesta (válido)
{
  "pokemon_name": "pikachu",
  "profile_name": "fast_attacker",
  "is_valid": true,
  "reason": "Validación exitosa. El Pokémon cumple con todos los requisitos del perfil."
}

# Respuesta (inválido)
{
  "pokemon_name": "charmander",
  "profile_name": "fast_attacker",
  "is_valid": false,
  "reason": "Falló en Ataque: Tiene 52 y el mínimo requerido es 80."
}
```

### Estructura del proyecto

```
orchestrator_api/
├── app/
│   ├── main.py                     # FastAPI app, registro de rutas
│   ├── api/
│   │   └── endpoints.py            # Endpoint /validate/{pokemon}/{profile}
│   ├── schemas/
│   │   └── pokemon.py              # Pydantic: PokemonValidationResponse
│   ├── services/
│   │   ├── poke_service.py         # GET a PokeAPI, extrae stats
│   │   ├── contract_service.py     # GET a Contract API, obtiene reglas
│   │   └── validator_service.py    # Lógica de validación contra perfil
│   └── core/
└── requirements.txt
```

---

## Contract API

API interna que expone los perfiles de validación (reglas de stats mínimos).

### Setup

```bash
cd contract_api
uvicorn app.main:app --reload --port 8000
```

### Endpoint

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/profiles/{name}` | Retorna un perfil con sus reglas |

### Perfiles disponibles

| Perfil | Reglas |
|--------|--------|
| `fast_attacker` | `min_attack: 80`, `min_speed: 90` |

```json
{
  "profile_name": "fast_attacker",
  "description": "Perfil diseñado para Pokémon con alto ataque y velocidad.",
  "rules": {
    "min_attack": 80,
    "min_speed": 90
  }
}
```

---

## DWH Analytics

Módulo independiente (no es un servicio HTTP). Conecta directamente a la PokeAPI con `requests`, construye DataFrames con `pandas` y genera archivos Parquet con un modelo dimensional Snowflake. Incluye consultas analíticas en SQL.

### Estructura

```
dwh_analytics/
├── generate_dwh_parquet.py     # ETL: extrae de PokeAPI, transforma y carga a Parquet
├── data/                       # Archivos Parquet del modelo dimensional
│   ├── dim_types.parquet
│   ├── dim_abilities.parquet
│   ├── dim_moves.parquet
│   ├── fact_pokemon_stats.parquet
│   ├── rel_pokemon_types.parquet
│   ├── rel_pokemon_abilities.parquet
│   └── rel_pokemon_moves.parquet
└── sql/                        # Consultas analíticas
    ├── pregunta_a.sql          # Top 3 tipos con mayor HP promedio
    ├── pregunta_b.sql          # Pokémon con earthquake + levitate
    ├── pregunta_c.sql          # Pokémon más rápido por tipo
    └── pregunta_d.sql          # Pokémon con >40 movimientos y >400 stats
```

### Ejecutar ETL

```bash
cd dwh_analytics
python generate_dwh_parquet.py
```

---

## Modelo Dimensional (Esquema Snowflake)

![Modelo Dimensional Snowflake](./docs/diagrama_dwh.png)

## Part 1: Data Warehouse & Dimensional Modeling (Snowflake Schema)

### Sustentación Técnica del Modelo

#### 1. Grano de la Tabla de Hechos (`fact_pokemon_stats`)
El grano de la tabla de hechos se define como **un registro por cada Pokémon individual evaluado**. 

* **Por qué se eligió este grano:** Las preguntas de negocio requeridas por el análisis (identificar al Pokémon con mayor ataque base, calcular el promedio de peso/altura por tipo y contar habilidades) se responden al nivel de entidad de un Pokémon único. No se requiere un grano transaccional (como "por intento de captura" o "por batalla"), sino un grano de estado instantáneo de las características base de cada criatura.
* **Métricas incluidas:** Almacena los valores numéricos aditivos y semi-aditivos que permiten agregaciones directas: `hp`, `attack`, `defense`, `special_attack`, `special_defense`, `speed`, `height` y `weight`.

---

#### 2. Resolución de Dimensiones Múltiples (Relaciones Muchos a Muchos)
Uno de los mayores retos de este modelo es que un Pokémon puede poseer **múltiples habilidades** y **múltiples movimientos**, lo que rompe la relación jerárquica estándar `1:N` de un esquema en estrella puro. Para resolver esto y mantener la integridad del modelo analítico, se implementó una estrategia de **Tablas de Hechos Puente (Bridge Tables)**, típica de la arquitectura Snowflake:

* **Cruce con Habilidades (`rel_pokemon_abilities`):** Se creó una tabla intermedia que conecta `fact_pokemon_stats` con la dimensión de habilidades. Cada registro representa la asignación de una habilidad específica a un Pokémon, incluyendo un atributo de contexto como `is_hidden` (si la habilidad es oculta).
* **Cruce con Movimientos (`rel_pokemon_moves`):** De igual manera, los movimientos se desacoplan mediante una tabla puente que mapea qué Pokémon puede aprender qué movimiento. Esto permite filtrar la tabla de hechos por cualquier atributo del movimiento (como su tipo o generación) sin duplicar las métricas físicas o de estadísticas del Pokémon en la tabla principal.
* **Cruce con Tipos (`rel_pokemon_types`):** Similar a las anteriores, maneja la relación muchos a muchos entre Pokémon y tipos, incluyendo el `slot` (posición del tipo) como atributo contextual.

---

## Setup General

### Requisitos

- Python 3.12+
- Las dependencias se gestionan desde `requirements.txt` en la raíz del proyecto

### Crear entorno virtual e instalar dependencias

```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux / WSL

pip install -r requirements.txt
```

### Ejecutar servicios (orden requerido)

```bash
# Terminal 1 - Contract API
cd contract_api
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Orchestrator API
cd orchestrator_api
uvicorn app.main:app --reload --port 8001
```

Ambos servicios deben estar corriendo simultáneamente para que el flujo de validación funcione correctamente.
