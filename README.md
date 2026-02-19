# Daily Trips Project - Plataforma de Datos AWS

## 1. Objetivo

Desarrollar un framework ETL/ELT reutilizable y automatizado para un
lakehouse en AWS, permitiendo procesar datasets de viajes diarios y
registrar resultados en S3 y Glue Data Catalog. La solución es
metadata-driven y configurable vía JSON/YAML.

------------------------------------------------------------------------

## 2. Arquitectura

Capas en S3:

Landing → Raw → Gold

Estructura del bucket: s3://jeff-data-lake-2026/ - landing/ - raw/ -
gold/ - logs/ - quality-reports/ - quarantine/ - config/

Procesamiento: - AWS Glue (PySpark) - Athena para consultas analíticas -
Glue Data Catalog para metadatos

------------------------------------------------------------------------

## 3. Estructura del Repositorio

daily-trips-aws-data-lake/ - src/ - framework/ - pipelines/ - config/ -
sql/ - doc/ - tests/ - README.md

------------------------------------------------------------------------

## 4. Configuración Metadata-Driven

Ejemplo JSON:

{ "source_bucket": "jeff-data-lake-2026", "landing_prefix": "landing/",
"raw_prefix": "raw/", "gold_prefix": "gold/", "partitions":
\["pickup_date"\], "quality_rules": \[ "completitud", "unicidad",
"rangos", "referencial", "outliers", "frescura" \], "incremental": true
}

------------------------------------------------------------------------

## 5. Guía de Ejecución

1.  Subir CSV a landing/
2.  Ejecutar Glue Job:

python src/pipelines/daily_trips_etl.py --pipeline
config/pipeline_trips.json

3.  Verificar outputs en raw/ y gold/
4.  Revisar quality-reports/
5.  Ejecutar consultas en Athena

------------------------------------------------------------------------

## 6. Validaciones de Calidad

-   Completitud
-   Unicidad
-   Rangos válidos
-   Consistencia referencial
-   Detección de outliers
-   Frescura de datos

------------------------------------------------------------------------

## 7. Control de Costos

-   Uso de Parquet
-   Particionamiento
-   Column pruning
-   Glue con máximo 2 DPU
-   Validación de bytes escaneados en Athena

------------------------------------------------------------------------

## 8. Evidencias

En carpeta doc/: - Glue Job Runs - Logs - Consulta Athena con bytes
escaneados - Outputs en S3 - Documento de diseño (2--4 páginas)

------------------------------------------------------------------------

Autor: Jefferson
