USE nyc_taxi_db;


--5 Consultas
-- 1️ Reparar particiones (sincronizar Glue Catalog)
MSCK REPAIR TABLE gold_fact_trips;

-- 2️ Conteo total de registros en capa Gold
SELECT COUNT(*) AS total_trips
FROM gold_fact_trips;

-- 3️ Conteo por partición (validación de particionamiento)
SELECT year, month, COUNT(*) AS num_registros
FROM gold_fact_trips
GROUP BY year, month
ORDER BY year, month;

-- 4️ Validación de duplicados (idempotencia)
SELECT trip_id, COUNT(*) AS duplicates
FROM gold_fact_trips
GROUP BY trip_id
HAVING COUNT(*) > 1;

-- 5️ Validación de unicidad total (consistencia)
SELECT COUNT(DISTINCT trip_id) AS unique_trips,
       COUNT(*) AS total_trips
FROM gold_fact_trips;
