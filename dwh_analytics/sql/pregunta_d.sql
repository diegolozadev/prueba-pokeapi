-- Pregunta D: Lista los nombres de los Pokémon que pueden aprender más de 40 movimientos 
-- distintos y cuya suma de estadísticas base (HP + Ataque + Defensa...) sea mayor a 400 puntos en total.

SELECT 
    f.nombre AS nombre_pokemon,
    -- Mostramos el conteo de movimientos y el total de estadísticas para que el reporte sea claro
    COUNT(DISTINCT rm.sk_move) AS total_movimientos,
    (f.hp + f.attack + f.defense + f.special_attack + f.special_defense + f.speed) AS total_stats
FROM fact_pokemon_stats f

-- Conexión con la tabla puente de movimientos usando la clave subrogada
INNER JOIN rel_pokemon_moves rm ON f.sk_pokemon = rm.sk_pokemon

-- Filtro a nivel de fila: Evaluamos la métrica horizontal de estadísticas base antes de agrupar
WHERE (f.hp + f.attack + f.defense + f.special_attack + f.special_defense + f.speed) > 400

-- Agrupamos por la clave primaria y el nombre del Pokémon para poder contar sus movimientos
GROUP BY f.sk_pokemon, f.nombre

-- Filtro a nivel de grupo: Conservamos solo los Pokémon que superen los 40 movimientos distintos
HAVING COUNT(DISTINCT rm.sk_move) > 400;