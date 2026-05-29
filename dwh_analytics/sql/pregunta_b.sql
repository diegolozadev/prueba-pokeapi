-- Pregunta B: Lista los nombres y la suma total de sus estadísticas base (Total Stats) 
-- de los Pokémon que pueden aprender el movimiento "earthquake" y que además poseen 
-- la habilidad "levitate", ordenados de mayor a menor poder.

SELECT 
    f.nombre AS nombre_pokemon,
    -- Sumamos todas las estadísticas base individuales para obtener el poder total
    (f.hp + f.attack + f.defense + f.special_attack + f.special_defense + f.speed) AS total_stats
FROM fact_pokemon_stats f

-- 1. Cruce con la dimensión de Movimientos a través de su tabla puente
INNER JOIN rel_pokemon_moves rm ON f.sk_pokemon = rm.sk_pokemon
INNER JOIN dim_moves m ON rm.sk_move = m.sk_move

-- 2. Cruce con la dimensión de Habilidades a través de su tabla puente
INNER JOIN rel_pokemon_abilities ra ON f.sk_pokemon = ra.sk_pokemon
INNER JOIN dim_abilities a ON ra.sk_ability = a.sk_ability

-- 3. Filtros específicos solicitados (Movimiento Y Habilidad)
WHERE m.move_name = 'earthquake'
  AND a.ability_name = 'levitate'

-- Ordenamos por el alias del cálculo matemático de mayor a menor poder
ORDER BY total_stats DESC;