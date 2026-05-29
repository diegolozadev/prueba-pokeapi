-- Pregunta C: Por cada Tipo de Pokémon, ¿cuál es el Pokémon con la estadística de 
-- 'Velocidad' (Speed) más alta? Muestra el Tipo, el Nombre del Pokémon y su Velocidad.

WITH ranked_pokemon_by_type AS (
    SELECT 
        t.type_name AS tipo_pokemon,
        f.nombre AS nombre_pokemon,
        f.speed AS velocidad,
        -- Window Function: Particiona los datos por cada tipo de Pokémon y los ordena 
        -- por velocidad de mayor a menor, asignando un número de fila único (ranking)
        ROW_NUMBER() OVER(
            PARTITION BY t.sk_type 
            ORDER BY f.speed DESC
        ) AS ranking_velocidad
    FROM fact_pokemon_stats f
    -- Conexión con la tabla puente de tipos
    INNER JOIN rel_pokemon_types r ON f.sk_pokemon = r.sk_pokemon
    -- Conexión con la dimensión final de tipos
    INNER JOIN dim_types t ON r.sk_type = t.sk_type
)
SELECT 
    tipo_pokemon,
    nombre_pokemon,
    velocidad
FROM ranked_pokemon_by_type
-- Filtramos para quedarnos únicamente con el Pokémon más rápido (Puesto 1) de cada tipo
WHERE ranking_velocidad = 1
-- Ordenamos el reporte final alfabéticamente por el tipo de Pokémon
ORDER BY tipo_pokemon ASC;