-- Pregunta A: ¿Cuáles son los 3 tipos de Pokémon con el mayor promedio de Puntos de Vida (HP)?

SELECT 
    t.type_name AS tipo_pokemon,          -- Nombre del tipo (ej. Fire, Water)
    ROUND(AVG(f.hp), 2) AS promedio_hp   -- Promedio de HP limitado a 2 decimales
FROM fact_pokemon_stats f

-- Conexión con la tabla puente usando la clave subrogada del Pokémon
INNER JOIN rel_pokemon_types r 
    ON f.sk_pokemon = r.sk_pokemon

-- Conexión con la dimensión final usando la clave subrogada del tipo
INNER JOIN dim_types t 
    ON r.sk_type = t.sk_type

-- Agrupación por identificador y nombre para calcular el promedio por cada tipo
GROUP BY t.sk_type, t.type_name

-- Ordenamos de mayor a menor promedio para dejar los más altos arriba
ORDER BY promedio_hp DESC

-- Filtramos para obtener únicamente el TOP 3 solicitado
LIMIT 3;